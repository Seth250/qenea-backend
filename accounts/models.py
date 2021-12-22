from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .messages import Messages
from .validators import MAX_USERNAME_LENGTH, validate_username

# Create your models here.

class User(PermissionsMixin, AbstractBaseUser):
    first_name = models.CharField(_('first name'), max_length=25)
    last_name = models.CharField(_('last name'), max_length=25)
    username = models.CharField(
        _('username'),
        unique=True, 
        max_length=MAX_USERNAME_LENGTH,
        validators=[validate_username],
        error_messages={
            'unique': Messages.NON_UNIQUE_USERNAME
        }
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': Messages.NON_UNIQUE_EMAIL
        }
    )
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
			'Designates whether this user should be treated as active.'
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
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.fullname

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'    

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[self.email], **kwargs)
