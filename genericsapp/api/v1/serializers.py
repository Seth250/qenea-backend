from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from genericsapp.models import Comment
from genericsapp.validators import validate_tag


# so that we can pass a list of strings (valid tag strings) to an object's tags field
class TagListSerializer(serializers.ListSerializer):
    child = serializers.SlugField()

    def __init__(self, *args, **kwargs):
        kwargs['allow_empty'] = False
        super().__init__(*args, **kwargs)
        self.child.validators.append(validate_tag)


class ContentTypeRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        return value.model

    def to_internal_value(self, data):
        return ContentType.objects.get(model=data)
    

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField()
    user = serializers.StringRelatedField()
    content_type = ContentTypeRelatedField(queryset=ContentType.objects.all())
    total_points = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ('url', 'user', 'content_type', 'object_id', 'content', 'total_points', 'created_at', 'updated_at')
