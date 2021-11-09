from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Profile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
        (OTHER, _('Other'))
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=250, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=2, default='')
    picture = models.ImageField(_('picture'), default='default_pp.png', upload_to='profile_pictures')
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    date_of_birth = models.DateField(_('date of birth'), blank=True, null=True)

    def __str__(self):
        return f'{self.user}\'s profile'

    def get_following_count(self):
        return self.following.count()

    def get_followers_count(self):
        return self.followers.count()
