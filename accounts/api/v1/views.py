from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http.response import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.encoding import (DjangoUnicodeDecodeError, smart_bytes,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse

from accounts.tasks import send_email

from .serializers import (AuthTokenSerializer, EmailRequestSerializer,
                          SetNewPasswordSerializer, UserCreateSerializer)

User = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    """
    Endpoint for new users to create accounts
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserCreateSerializer


class ObtainAuthTokenAPIView(views.APIView):
    """
    Endpoint to login registered users (obtain authentication token)
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = AuthTokenSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'auth_token': token.key,
            'username': user.username
        }
        return Response(data=data, status=status.HTTP_200_OK)


class AuthTokenDestroyAPIView(views.APIView):
    """
    Endpoint to logout users (delete authentication token)
    """
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RequestPasswordResetEmailAPIView(generics.GenericAPIView):
    """
    Endpoint for registered users to request a password reset
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = EmailRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        if user:
            email = serializer.validated_data['email']
            subject = 'Reset Your Qenea Password'
            # we pass request so that reverse can return the absolute url and not just the relative path
            password_reset_confirm_url = api_reverse(
                'Accounts_API_v1:password-reset-confirm',
                kwargs={
                    'uidb64': urlsafe_base64_encode(smart_bytes(user.id)),
                    'token': PasswordResetTokenGenerator().make_token(user)
                },
                request=request
            )
            context = {
                'user_firstname': user.first_name,
                'password_reset_confirm_url': password_reset_confirm_url
            }
            html_content = render_to_string('accounts/password_reset_email.html', context=context, request=request)
            text_content = render_to_string('accounts/password_reset_email.txt', context=context, request=request)

            # .delay() makes the celery task run in the background
            send_email.delay(subject=subject, body=text_content, to=email, html_content=html_content)

        msg = 'If an account exists, you would receive an email with further instructions.'
        return Response(data={'message': msg}, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(views.APIView):
    """
    Endpoint to ensure that uidb64 and token are valid
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        try:
            uidb64 = kwargs['uidb64']
            token = kwargs['token']
            id_ = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id_)

            if not PasswordResetTokenGenerator().check_token(user=user, token=token): # if token has already been used
                # TODO: add custom error page or redirect to frontend error page when created
                return Response(status=status.HTTP_403_FORBIDDEN)

            frontend_confirm_url = f'{settings.BASE_FRONTEND_URL}/password-reset/confirm/{uidb64}/{token}/'
            return HttpResponseRedirect(frontend_confirm_url)

        except DjangoUnicodeDecodeError:
            # TODO: add custom error page or redirect to frontend error page when created
            return Response(status=status.HTTP_403_FORBIDDEN)


class SetNewPasswordAPIView(generics.GenericAPIView):
    """
    Endpoint to set the user's new password
    """
    serializer_class = SetNewPasswordSerializer
    permission_classes = (permissions.AllowAny, )

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Password has been reset successfully!'}, status=status.HTTP_200_OK)
