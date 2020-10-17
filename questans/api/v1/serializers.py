from rest_framework import serializers
from questans.models import Question, Answer, Comment
from rest_framework.reverse import reverse as api_reverse


class CommentObjectRelatedField(serializers.RelatedField):
	"""
	A custom field to use for the `comment_object` generic relationship.
	"""
	def to_representation(self, value):
		if isinstance(value, Question):
			return f'Question: {value.id}'

		elif isinstance(value, Answer):
			return f'Answer: {value.id}'
		
		raise Exception('Unexpected type of comment object')


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='Questions-API:answer-detail')
	user = serializers.PrimaryKeyRelatedField(read_only=True)
	comments = CommentObjectRelatedField(many=True, read_only=True)
	question = serializers.HyperlinkedRelatedField(
		view_name='Questions-API:question-detail', 
		queryset=Question.objects.all(), 
		lookup_field='slug'
	)

	class Meta:
		model = Answer
		fields = (
			'id', 'url', 'user', 'question', 'content', 'accepted', 'upvotes', 'downvotes', 'total_points', 
			'comments', 'date_created'
		)
		read_only_fields = ('user', 'upvotes', 'downvotes')


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
	# explicitly redefining the url field because the lookup for the view name fails if we don't define it
	# also explicitly redefining the user and comments field because they also failed to work right off the bat
	# url = serializers.HyperlinkedIdentityField(read_only=True, view_name='Questions-API:question-detail')
	url = serializers.HyperlinkedIdentityField(view_name='Questions-API:question-detail', lookup_field='slug')
	user = serializers.PrimaryKeyRelatedField(read_only=True)
	comments = CommentObjectRelatedField(many=True, read_only=True)
	answers = AnswerSerializer(many=True, read_only=True)

	class Meta:
		model = Question
		fields = (
			'id', 'url', 'user', 'slug', 'title', 'description', 'upvotes', 'downvotes', 'total_points', 'answers',
			'comments', 'date_posted'
		)
		read_only_fields = ('id', 'upvotes', 'downvotes', 'date_posted')
