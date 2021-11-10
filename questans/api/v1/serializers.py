from rest_framework import serializers

from questans.models import Question


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='Questans_API_v1:question-detail',
        lookup_field='slug'
    )
    user = serializers.StringRelatedField()
    total_points = serializers.ReadOnlyField()

    class Meta:
        model = Question
        fields = ('url', 'user', 'slug', 'title', 'description', 'total_points', 'created_at', 'updated_at')
