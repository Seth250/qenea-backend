from rest_framework import serializers

from accounts.api.v1.serializers import UserSerializer
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    following_count = serializers.IntegerField(source='get_following_count', read_only=True)
    followers_count = serializers.IntegerField(source='get_followers_count', read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'gender', 'picture', 'following_count', 'followers_count', 'date_of_birth')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.username = user_data.get('username', user.username)
            user.save()

        instance.bio = validated_data.get('bio', instance.bio)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()

        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if self.context['request'].method == 'GET':
            ret['gender_choices'] = instance.GENDER_CHOICES

        return ret
