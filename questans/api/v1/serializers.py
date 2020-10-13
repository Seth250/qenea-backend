from rest_framework import serializers
from questans.models import Question, Answer, Comment


class QuestionSerializer(serializers.ModelSerializer):

	class Meta:
		model = Question
		fields = ('id', 'user', 'slug', 'title', 'description', )
		read_only_fields = ('id', 'user', 'slug')
