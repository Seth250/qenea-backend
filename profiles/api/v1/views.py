from .serializers import ProfileSerializer
from rest_framework import mixins, viewsets
from questans.api.v1.permissions import CustomModelPermissions
from profiles.models import Profile


class ProfileViewSet(mixins.ListModelMixin,
					 mixins.RetrieveModelMixin,
					 mixins.UpdateModelMixin,
					 viewsets.GenericViewSet):
	serializer_class = ProfileSerializer
	permission_classes = (CustomModelPermissions, )

	def get_queryset(self):
		return Profile.objects.all()

	def perform_create(self, serializer):
		return serializer.save(user=self.request.user)