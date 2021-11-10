from rest_framework import serializers

from questans.models import Question
from questans.validators import validate_tag


# so that we can pass a list of strings (valid tag strings) to an object's tags field
class TagListSerializer(serializers.ListSerializer):
    child = serializers.SlugField()

    def __init__(self, *args, **kwargs):
        kwargs['allow_empty'] = False
        super().__init__(*args, **kwargs)
        self.child.validators.append(validate_tag)


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

