from .serializers import ProfileSerializer
from rest_framework.viewsets import ModelViewSet
from questans.api.v1.permissions import CustomModelPermissions


class ProfileViewSet(ModelViewSet):
	serializer_class = ProfileSerializer
	permission_classes = (CustomModelPermissions, )

	def get_queryset(self):
		return Profile.objects.all()

	def perform_create(self, serializer):
		return serializer.save(user=self.request.user)