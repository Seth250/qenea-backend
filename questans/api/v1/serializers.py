from rest_framework import serializers
from questans.models import Question, Answer, Comment


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


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
	# explicitly redefining the url field because the lookup for the view name fails if we don't define it
	# also explicitly redefining the user and comments field because they also failed to work right off the bat
	url = serializers.HyperlinkedIdentityField(read_only=True, view_name='Questions-API:question-detail')
	user = serializers.PrimaryKeyRelatedField(read_only=True)
	comments = CommentObjectRelatedField(many=True, read_only=True)

	class Meta:
		model = Question
		fields = (
			'id', 'url', 'user', 'slug', 'title', 'description', 'upvotes', 'downvotes', 'total_points', 'answers',
			'comments'
		)
		read_only_fields = ('id', 'slug', 'upvotes', 'downvotes', 'total_points', 'answers')