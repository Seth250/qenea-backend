from rest_framework import serializers
from questans.models import Question, Answer, Comment


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
	# explicitly defining the uri field because the lookup for the view name fails if we don't define it
	uri = serializers.HyperlinkedIdentityField(read_only=True, view_name='Questions-API:question-detail')
	user = serializers.PrimaryKeyRelatedField(read_only=True)

	class Meta:
		model = Question
		fields = (
			'id', 'uri', 'user', 'slug', 'title', 'description', 'upvotes', 'downvotes', 'total_points', 'answers'
		)
		read_only_fields = ('id', 'slug', 'upvotes', 'downvotes', 'total_points', 'answers')