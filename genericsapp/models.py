from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='comments')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.CharField(max_length=200)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='upvoted_comments')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='downvoted_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user}'s comment"

    @property
    def total_points(self):
        return self.upvotes.count() - self.downvotes.count()
