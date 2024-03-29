import uuid

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.text import slugify

from comments.models import Comment

# Create your models here.


class Tag(models.Model):
    name = models.SlugField()

    def __str__(self):
        return self.name


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=120)
    # if you use uuid field (not as primary key) in another project and you encounter unique constraint errors 
    # with uuid, check /howto/writing-migrations/#migrations-that-add-unique-fields in django docs
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=150, default='', editable=False, unique=True)
    description = models.TextField()
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='questions_upvoted')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='questions_downvoted')
    tags = models.ManyToManyField(Tag, related_name='questions')
    comments = GenericRelation(Comment)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify('%s-%s' % (self.title, self.uuid), allow_unicode=True)
        return super(Question, self).save(*args, **kwargs)

    @property
    def total_points(self):
        return self.upvotes.count() - self.downvotes.count()

    @property
    def total_answers(self):
        return self.answers.count()

    def get_description_summary(self):
        return f'{self.description[:150]}...'


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='answers_upvoted')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='answers_downvoted')
    comments = GenericRelation(Comment)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user}'s answer"

    @property
    def total_points(self):
        return self.upvotes.count() - self.downvotes.count()
