from rest_framework import serializers
from rest_framework.reverse import reverse as api_reverse

from accounts.api.v1.serializers import UserSerializer
from profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    following_count = serializers.ReadOnlyField(source='get_following_count')
    followers_count = serializers.ReadOnlyField(source='get_followers_count')

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


class ProfileFollowSerializer(serializers.Serializer):
    user = UserSerializer()
    picture = serializers.ImageField()
    profile_url = serializers.SerializerMethodField()
    follow_toggle_url = serializers.SerializerMethodField()
    is_followed_by_viewer = serializers.SerializerMethodField()

    def get_profile_url(self, obj):
        request = self.context['request']
        return api_reverse('Profiles_API_v1:profile-detail', kwargs={'username': obj.user.username}, request=request)

    def get_follow_toggle_url(self, obj):
        request = self.context['request']
        return api_reverse('Profiles_API_v1:follow-toggle', kwargs={'pk': obj.pk}, request=request)

    def get_is_followed_by_viewer(self, obj):
        user_profile = self.context['request'].user.profile
        return user_profile.following.filter(pk=obj.pk).exists()
