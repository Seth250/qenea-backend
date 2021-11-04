import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify

# Create your models here.


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=120)
    # if you use uuid field (not as primary key) in another project and you encounter unique constraint errors 
    # with uuid, check /howto/writing-migrations/#migrations-that-add-unique-fields in django docs
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=150, default='', editable=False, unique=True)
    description = models.TextField()
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='question_upvotes')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='question_downvotes')
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify('%s-%s' % (self.title, self.uuid), allow_unicode=True)
        return super(Question, self).save(*args, **kwargs)

    def get_total_points(self):
        return self.upvotes.count() - self.downvotes.count()


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='answer_upvotes')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='answer_downvotes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user}'s answer"

    def get_total_points(self):
        return self.upvotes.count() - self.downvotes.count()



