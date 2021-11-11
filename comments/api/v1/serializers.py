from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from comments.models import Comment


class ContentTypeRelatedField(serializers.RelatedField):

    def to_internal_value(self, data):
        return ContentType.objects.get(model=data)

    def to_representation(self, instance):
        return instance.model


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='Comments_API_v1:comment-detail')
    user = serializers.StringRelatedField()
    content_type = ContentTypeRelatedField(queryset=ContentType.objects.all())
    total_points = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ('url', 'user', 'content_type', 'object_id', 'content', 'total_points', 'created_at', 'updated_at')
