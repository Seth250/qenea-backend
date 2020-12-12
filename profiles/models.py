from django.db import models
from django.conf import settings

# Create your models here.


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	image = models.ImageField(default='default_pp.png', upload_to='profile_pictures')
	bio = models.TextField(max_length=500, blank=True)
	date_of_birth = models.DateField(blank=True, null=True)

	class Meta:
		ordering = ['user__date_joined']

	def __str__(self):
		return f"{self.user}'s Profile"
