from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class User(PermissionsMixin, AbstractBaseUser):
	first_name = models.CharField(_('first name'), max_length=30)
	last_name = models.CharField(_('last name'), max_length=30)
	email = models.EmailField(
		_('email address'), 
		unique=True, 
		error_messages={
			'unique': _('A user with that email already exists.')
		})
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	is_active = models.BooleanField(
		_('active'), 
		default=True,
		help_text=_(
			'Designates whether this user should be treated as active. '
			'Unselect this instead of deleting accounts.'
		)
	)
	is_staff = models.BooleanField(
		_('staff status'), 
		default=False, 
		help_text=_('Designates whether the user can log into the admin site.')
	)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['first_name', 'last_name']

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	def __str__(self):
		return self.full_name

	@property
	def full_name(self):
		return f'{self.first_name} {self.last_name}'

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)
