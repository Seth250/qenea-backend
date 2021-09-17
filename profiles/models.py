from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Profile(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    GENDER = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (OTHER, _('Other'))
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(_('username'), max_length=25, unique=True)
    gender = models.CharField(choices=GENDER, max_length=10, default='')
    bio = models.CharField(max_length=500, blank=True)
    date_of_birth = models.DateTimeField(_('date of birth'), blank=True, null=True)

    def __str__(self):
        return self.username
