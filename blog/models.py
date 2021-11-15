from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone

from comments.models import Comment
from questans.models import Tag

# Create your models here.


class PostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(status='pd').order_by('-published_at')

    def drafted(self):
        return self.filter(status='dt').order_by('-updated_at')


class Post(models.Model):
    DRAFT = 'dt'
    PUBLISHED = 'pd'
    POST_CHOICES = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.TextField()
    comments = GenericRelation(Comment)
    status = models.CharField(max_length=3, choices=POST_CHOICES, default=DRAFT)
    tags = models.ManyToManyField(Tag, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def publish(self):
        self.status = self.PUBLISHED
        self.published_at = timezone.now()

