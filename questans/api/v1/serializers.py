from rest_framework import serializers

from questans.models import Question


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.SlugRelatedField(many=True, slug_field='name')
    total_points = serializers.ReadOnlyField(source='get_total_points')

    class Meta:
        model = Question
        fields = ('slug', 'title', 'description', 'tags', 'total_points', 'created_at', 'updated_at')
