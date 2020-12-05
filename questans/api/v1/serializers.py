from rest_framework import serializers
from questans.models import Question, Answer, Comment
from rest_framework.reverse import reverse as api_reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from accounts.api.v1.serializers import UserSerializer


UserModel = get_user_model()

class ContentTypeRelatedField(serializers.RelatedField):

	def to_representation(self, obj):
		return obj.model

	def to_internal_value(self, data):
		return ContentType.objects.get(model=data)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
	# hyperlinked identity fields are read_only by default
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
	comments = CommentSerializer(many=True, read_only=True)

	class Meta:
		model = Answer
		fields = (
			'id', 'url', 'user', 'question', 'content', 'accepted', 'upvotes', 'downvotes', 'total_points', 
			'comments', 'date_created', 'date_updated'
		)
		read_only_fields = ('id', 'upvotes', 'downvotes')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='Questans-API:question-detail', lookup_field='slug')
	user = serializers.PrimaryKeyRelatedField(read_only=True)
	upvotes = serializers.StringRelatedField(many=True, read_only=True)
	downvotes = serializers.StringRelatedField(many=True, read_only=True)
	answers = AnswerSerializer(many=True, read_only=True)
	comments = CommentSerializer(many=True, read_only=True)

	class Meta:
		model = Question
		fields = (
			'id', 'url', 'user', 'slug', 'title', 'description', 'upvotes', 'downvotes', 'total_points', 
			'answers', 'comments', 'date_posted', 'date_updated'
		)
		read_only_fields = ('id', 'upvotes', 'downvotes', 'date_posted', 'date_updated')
