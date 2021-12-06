from typing import List

from django.db import transaction

from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from accounts.api.v1.serializers import ObjectUserSerializer
from questans.models import Answer, Question, Tag
from questans.validators import validate_tag


# custom list serializer to enable passing a list of strings (valid tag strings) to an object's tags field
class TagListSerializer(serializers.ListSerializer):
    child = serializers.CharField()

    def __init__(self, *args, **kwargs):
        kwargs['allow_empty'] = False
        super().__init__(*args, **kwargs)
        self.child.validators.append(validate_tag)


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='Questans_API_v1:question-detail',
        lookup_field='slug'
    )
    user = ObjectUserSerializer()
    total_points = serializers.ReadOnlyField()
    tags = TagListSerializer()
    comments = serializers.SerializerMethodField(method_name='get_comments_url')

    class Meta:
        model = Question
        fields = ('url', 'user', 'slug', 'title', 'description', 'total_points', 'tags', 'comments', 'created_at', 'updated_at')

    def create(self, validated_data):
        tags_data: List[str] = validated_data.pop('tags')
        instance = Question.objects.create(**validated_data)
        tag_objects = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_data]
        instance.tags.set(tag_objects)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        tags_data: List[str] = validated_data.pop('tags')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        tag_objects = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_data]
        instance.tags.set(tag_objects)
        return instance

    def get_comments_url(self, obj):
        request = self.context['request']
        return api_reverse('Questans_API_v1:question-comments', kwargs={'slug': obj.slug}, request=request)


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='Questans_API_v1:answer-detail')
    user = ObjectUserSerializer()
    question = serializers.HyperlinkedRelatedField(
        view_name='Questans_API_v1:question-detail',
        queryset=Question.objects.all(),
        lookup_field='slug'
    )
    total_points = serializers.ReadOnlyField()
    comments = serializers.SerializerMethodField(method_name='get_comments_url')

    class Meta:
        model = Answer
        fields = ('url', 'user', 'question', 'content', 'is_accepted', 'total_points', 'comments', 'created_at', 'updated_at')

    def get_comments_url(self, obj):
        request = self.context['request']
        return api_reverse('Questans_API_v1:answer-comments', kwargs={'slug': obj.slug}, request=request)
