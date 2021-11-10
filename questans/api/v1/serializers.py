from rest_framework import serializers

from questans.models import Question


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    total_points = serializers.ReadOnlyField()

    class Meta:
        model = Question
        fields = ('slug', 'title', 'description', 'total_points', 'created_at', 'updated_at')
