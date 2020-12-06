from .serializers import QuestionSerializer, AnswerSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
# from rest_framework import permissions
from .permissions import CustomModelPermissions
from django.views.generic.detail import SingleObjectMixin
from questans.models import Question, Answer, Comment
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView


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


class ObjectActionToggleAPIView(SingleObjectMixin, APIView):
	permission_classes = (permissions.IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		obj = self.get_object()
		main_manager, opp_manager = (obj.upvotes, obj.downvotes) if self.action == 'upvote' else (obj.downvotes, obj.upvotes)
		if request.user in main_manager.all():
			main_manager.remove(request.user)

		else:
			main_manager.add(request.user)
			if request.user in opp_manager.all():
				opp_manager.remove(request.user)

		obj.save() # so that it would call the object's save method and update the total points
		return Response(status=status.HTTP_200_OK)


class QuestionUpvoteAPIView(ObjectActionToggleAPIView):
	model = Question
	action = 'upvote'


class QuestionDownvoteAPIView(ObjectActionToggleAPIView):
	model = Question
	action = 'downvote'
