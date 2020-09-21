from django.db import models
from django.conf import settings

# Create your models here.

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions',
                             related_query_name='question')
    title = models.CharField(max_length=150)
    description = models.TextField()
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='question_upvotes')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='question_downvotes')