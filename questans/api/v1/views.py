from .serializers import QuestionSerializer, AnswerSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import CustomModelPermissions
from questans.models import Question, Answer, Comment


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


class CommentViewSet(ModelViewSet):
	serializer_class = CommentSerializer
	permission_classes = (CustomModelPermissions, )

	def get_queryset(self):
		return Comment.objects.all()

	def perform_create(self, serializer):
		return serializer.save(user=self.request.user)
