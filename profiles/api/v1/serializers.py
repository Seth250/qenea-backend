from profiles.models import Profile
from rest_framework import serializers
from accounts.api.v1.serializers import UserSerializer


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="Profiles-API:profile-detail")
	# user = serializers.PrimaryKeyRelatedField(read_only=True)
	user = UserSerializer(read_only=True)

	class Meta:
		model = Profile
		fields = ('id', 'url', 'user', 'bio', 'image', 'date_of_birth')
		read_only_fields = ('id', )

	def create(self, validated_data):
		print(validated_data)
		return validated_data