from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions',
                            related_query_name='question')
    title = models.CharField(max_length=150)
    slug = models.CharField(default='', max_length=150, editable=False)
    description = models.TextField()
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='question_upvotes')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='question_downvotes')
    total_points = models.IntegerField(default=0, editable=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.total_points = self.upvotes.count() - self.downvotes.count()
        return super(Question, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.pk, 'slug': self.slug})


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers', 
                            related_query_name='answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', 
                            related_query_name='answer')
    content = models.TextField()
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='answer_upvotes')
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='answer_downvotes')
    accepted = models.BooleanField(default=False)
    total_points = models.IntegerField(default=0)

