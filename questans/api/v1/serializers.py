from rest_framework import serializers
from questans.models import Question, Answer, Comment
from rest_framework.reverse import reverse as api_reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from accounts.api.v1.serializers import UserSerializer
from django.core.paginator import Paginator


UserModel = get_user_model()

class ContentTypeRelatedField(serializers.RelatedField):

	def to_representation(self, obj):
		return obj.model

	def to_internal_value(self, data):
		return ContentType.objects.get(model=data)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
	# hyperlinked identity fields are implicitly read_only
	url = serializers.HyperlinkedIdentityField(view_name='Questans-API:comment-detail')
	user = serializers.PrimaryKeyRelatedField(read_only=True)
	# content_type = serializers.SlugRelatedField(queryset=ContentType.objects.all(), slug_field='model')
	content_type = ContentTypeRelatedField(queryset=ContentType.objects.all())

	class Meta:
		model = Comment
		fields = (
			'id', 'url', 'user', 'content', 'content_type', 'object_id', 'upvotes', 'downvotes', 'total_points', 
			'date_created'
		)
		read_only_fields = ('id', 'user', 'upvotes', 'downvotes')


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='Questans-API:answer-detail')
	user = serializers.PrimaryKeyRelatedField(read_only=True)
	question = serializers.HyperlinkedRelatedField(
		view_name='Questans-API:question-detail', 
		queryset=Question.objects.all(), 
		lookup_field='slug'
	)
	# serializer method field is implicitly read_only
	comments = serializers.SerializerMethodField(method_name='get_comments_url', read_only=True)
	# comments = CommentSerializer(many=True, read_only=True)

	class Meta:
		model = Answer
		fields = (
			'id', 'url', 'user', 'question', 'content', 'accepted', 'upvotes', 'downvotes', 'total_points', 
			'comments', 'date_created', 'date_updated'
		)
		read_only_fields = ('id', 'upvotes', 'downvotes')

	def get_comments_url(self, obj):
		request = self.context['request']
		return api_reverse('Questans-API:answer-comments', kwargs={'pk': obj.pk}, request=request)


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='Questans-API:question-detail', lookup_field='slug')
	user = serializers.PrimaryKeyRelatedField(read_only=True)
	upvotes = serializers.StringRelatedField(many=True, read_only=True)
	downvotes = serializers.StringRelatedField(many=True, read_only=True)
	answers =  serializers.SerializerMethodField(method_name='get_paginated_answers')
	# answers = AnswerSerializer(many=True, read_only=True)
	# comments = CommentSerializer(many=True, read_only=True)
	comments = serializers.SerializerMethodField(method_name='get_comments_url')

	class Meta:
		model = Question
		fields = (
			'id', 'url', 'user', 'slug', 'title', 'description', 'upvotes', 'downvotes', 'total_points', 
			'answers', 'comments', 'date_posted', 'date_updated'
		)
		read_only_fields = ('id', 'upvotes', 'downvotes', 'date_posted', 'date_updated')

	def get_paginated_answers(self, obj):
		request = self.context['request']
		# number of items per page
		page_size = request.query_params.get('size') or 5
		paginator = Paginator(obj.answers.all(), page_size)
		# page number for the question's answers pagination.
		# I'm using 'answer-page' instead of the typical 'page' as the page query parameter to prevent possible
		# conflicts with the question list endpoint (since this is a nested pagination).
		page_number = request.query_params.get('answer-page') or 1
		page = paginator.page(page_number)
		serializer = AnswerSerializer(page, many=True, context={'request': request})
		question_url = api_reverse('Questans-API:question-detail', kwargs={'slug': obj.slug}, request=request)

		next_url = f"{question_url}?answer-page={page.next_page_number()}" if page.has_next() else None
		if page.has_previous():
			previous_page_number = page.previous_page_number()
			previous_url = f"{question_url}{f'?answer-page={previous_page_number}' if previous_page_number != 1 else ''}"

		else:
			previous_url = None

		response = {
			"count": page.paginator.count,
			"next": next_url,
			"previous": previous_url,
			"results": serializer.data
		}
		return response

	def get_comments_url(self, obj):
		request = self.context['request']
		return api_reverse('Questans-API:question-comments', kwargs={'slug': obj.slug}, request=request)
