from profiles.models import Profile
from rest_framework import serializers
from accounts.api.v1.serializers import SerializerUsernameField, UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    username = SerializerUsernameField()
    following_count = serializers.IntegerField(source='get_following_count', read_only=True)
    followers_count = serializers.IntegerField(source='get_followers_count', read_only=True)
    # use options request to get the list of choices for gender

    class Meta:
        model = Profile
        fields = ('id', 'user', 'username', 'picture', 'gender', 'following_count', 'followers_count', 'bio', 'date_of_birth')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            instance.user.first_name = user_data.get('first_name', instance.user.first_name)
            instance.user.last_name = user_data.get('last_name', instance.user.last_name)

        instance.username = validated_data.get('username', instance.username)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()

        return instance