from profiles.models import Profile
from rest_framework import serializers


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name="profiles-API:profile-detail")
	user = serializers.PrimaryKeyRelatedField(read_only=True)

	class Meta:
		model = Profile
		fields = ('id', 'url', 'user', 'bio', 'date_of_birth')
		read_only_fields = ('id', )