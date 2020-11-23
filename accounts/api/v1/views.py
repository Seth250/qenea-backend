from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return get_user_model().objects.all()


class UserListRetrieveViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_queryset(self):
        return get_user_model().objects.all()


class UserLogoutAPIView(APIView):
	permission_classes = (permissions.IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		print(request.user.auth_token)
		return Response(status=status.HTTP_204_NO_CONTENT)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
	"""
	Handles password reset tokens
	When a token is created, an e-mail needs to be sent to the user
	:param sender: View Class that sent the signal
	:param instance: View Instance that sent the signal
	:param reset_password_token: Token Model Object
	:param args:
	:param kwargs:
	:return:
	"""
	current_site = get_current_site(request=None)

	# send an email to the user
	context = {
		'current_user': reset_password_token.user,
		'username': reset_password_token.user.username,
		'email': reset_password_token.user.email,
		'reset_password_url': f"{reverse('password_reset:reset-password-request')}?token={reset_password_token.key}",
		'domain': current_site.domain,
		'protocol': 'http'
	}

	# render email text
	email_html_message = render_to_string('accounts/user_reset_password.html', context)
	print(email_html_message)
	email_plaintext_message = render_to_string('accounts/user_reset_password.txt', context)

	msg = EmailMultiAlternatives(
		# title:
		"Password Reset for Qenea",
		# message:
		email_plaintext_message,
		# from:
		"noreply@localhost",
		# to:
		[reset_password_token.user.email]
	)
	msg.attach_alternative(email_html_message, 'text/html')
	# msg.send()
