from .serializers import QuestionSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import CustomModelPermissions
from questans.models import Question


class QuestionViewSet(ModelViewSet):
	serializer_class = QuestionSerializer
	permission_classes = (CustomModelPermissions, )

	def get_queryset(self):
		return Question.objects.all()

	def perform_create(self, serializer):
		return serializer.save(user=self.request.user)
