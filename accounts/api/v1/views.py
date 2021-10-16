from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse

from accounts.tasks import send_email

from .serializers import (AuthTokenSerializer, EmailRequestSerializer,
                          UserCreateSerializer)

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
            'email': user.email
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
            protocol = request.scheme,
            domain = get_current_site(request=request).domain
            confirm_url = api_reverse(
                'Accounts_API_v1:password-reset-confirm',
                kwargs={
                    'uidb64': urlsafe_base64_encode(smart_bytes(user.id)),
                    'token': PasswordResetTokenGenerator().make_token(user)
                }
            )
            password_reset_confirm_url = f'{protocol}://{domain}{confirm_url}'
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
