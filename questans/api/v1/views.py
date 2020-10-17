from .serializers import QuestionSerializer, AnswerSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import CustomModelPermissions
from questans.models import Question, Answer


class QuestionViewSet(ModelViewSet):
	serializer_class = QuestionSerializer
	permission_classes = (CustomModelPermissions, )
	lookup_field = 'slug'

	def get_queryset(self):
		return Question.objects.all()

	def perform_create(self, serializer):
		return serializer.save(user=self.request.user)


class AnswerViewSet(ModelViewSet):
	serializer_class = AnswerSerializer
	permission_classes = (CustomModelPermissions, )

	def get_queryset(self):
		return Answer.objects.all()

	def perform_create(self, serializer):
		return serializer.save(user=self.request.user)
