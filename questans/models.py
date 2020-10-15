from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from rest_framework.reverse import reverse as api_reverse


# Create your models here.

class Comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	content = models.TextField()
	upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_upvotes')
	downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='comment_downvotes')
	total_points = models.IntegerField(default=0, editable=False)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering = ['date_created']

	def save(self, *args, **kwargs):
		if self.id:
			self.total_points = self.upvotes.count() - self.downvotes.count()

		return super(Comment, self).save(*args, **kwargs)


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
	comments = GenericRelation(Comment)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if self.id:
			self.total_points = self.upvotes.count() - self.downvotes.count()

		self.slug = slugify(self.title, allow_unicode=True)
		return super(Question, self).save(*args, **kwargs)

	# def get_absolute_url(self):
	# 	return reverse('question_detail', kwargs={'pk': self.pk, 'slug': self.slug})


class Answer(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='answers', 
							related_query_name='answer')
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', 
							related_query_name='answer')
	content = models.TextField()
	accepted = models.BooleanField(default=False)
	upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='answer_upvotes')
	downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='answer_downvotes')
	total_points = models.IntegerField(default=0, editable=False)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	comments = GenericRelation(Comment)

	class Meta:
		ordering = ['-date_created']

	def save(self, *args, **kwargs):
		if self.id:
			self.total_points = self.upvotes.count() - self.downvotes.count()

		return super(Answer, self).save(*args, **kwargs)
