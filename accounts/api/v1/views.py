from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.utils.encoding import (DjangoUnicodeDecodeError, smart_bytes,
                                   smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.safestring import mark_safe

from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from accounts.tasks import send_email

from .serializers import (AuthTokenSerializer, EmailRequestSerializer,
                          SetNewPasswordSerializer, UserCreateSerializer,
                          UsernameValidateSerializer)

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

    @extend_schema(request=None, responses={'204': None}) # for schema warnings since view has no serializer
    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UsernameValidateAPIView(views.APIView):
    """
    Dedicated endpoint to validate username
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = UsernameValidateSerializer

    @extend_schema(responses={'204': None})
    def get(self, request, *args, **kwargs):
        data = {'username': kwargs['username']}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
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
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            frontend_confirm_url = f'{settings.BASE_FRONTEND_URL}/password-reset/confirm/?u={uidb64}&t={token}'
            context = {
                'user_firstname': user.first_name,
                'password_reset_confirm_url': mark_safe(frontend_confirm_url) # prevents ampersand(&) from being html encoded as &amp;
            }
            html_content = render_to_string('accounts/password_reset_email.html', context=context, request=request)
            text_content = render_to_string('accounts/password_reset_email.txt', context=context, request=request)

            # .delay() makes the celery task run in the background
            send_email.delay(subject=subject, body=text_content, to=email, html_content=html_content)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(views.APIView):
    """
    Endpoint to check whether uidb64 and token from the frontend are valid (they would also be
    checked in the /complete request).

    The frontend would only show the password reset form if both are valid
    """
    permission_classes = (permissions.AllowAny, )

    @extend_schema(request=None, responses={'204': None})
    def get(self, request, *args, **kwargs):
        try:
            uidb64 = kwargs['uidb64']
            token = kwargs['token']
            id_ = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id_)

            if not PasswordResetTokenGenerator().check_token(user=user, token=token): # if token has already been used
                return Response(status=status.HTTP_403_FORBIDDEN)

            return Response(status=status.HTTP_204_NO_CONTENT)

        except DjangoUnicodeDecodeError:
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
        return Response(data=serializer.data, status=status.HTTP_200_OK)
