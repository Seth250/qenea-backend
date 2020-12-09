from .serializers import QuestionSerializer, AnswerSerializer, CommentSerializer
from rest_framework.viewsets import ModelViewSet
# from rest_framework import permissions
from .permissions import CustomModelPermissions
from django.views.generic.detail import SingleObjectMixin
from questans.models import Question, Answer, Comment
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action


class ObjectCommentsViewSetActionMixin:

	@action(methods=['GET'], detail=True)
	def comments(self, request, *args, **kwargs):
		obj = self.get_object()
		comments = obj.comments.order_by('date_created')

		page = self.paginate_queryset(comments)
		if page is not None:
			serializer = CommentSerializer(page, many=True, context={'request': request})
			return self.get_paginated_response(serializer.data)

		serializer = CommentSerializer(comments, many=True, context={'request': request})
		return Response(serializer.data)


class QuestionViewSet(ObjectCommentsViewSetActionMixin, ModelViewSet):
	serializer_class = QuestionSerializer
	permission_classes = (CustomModelPermissions, )
	lookup_field = 'slug'

	def get_queryset(self):
		return Question.objects.all()

	def perform_create(self, serializer):
		return serializer.save(user=self.request.user)


class AnswerViewSet(ObjectCommentsViewSetActionMixin, ModelViewSet):
	serializer_class = AnswerSerializer
	permission_classes = (CustomModelPermissions, )

	def get_queryset(self):
		print('lol')
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

	def get_action_managers(self):
		action = self.kwargs.get('action')
		if action == 'upvote-toggle':
			return (self.object.upvotes, self.object.downvotes)

		elif action == 'downvote-toggle':
			return (self.object.downvotes, self.object.upvotes)

		return Response(status=status.HTTP_404_NOT_FOUND)

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		main_manager, opp_manager = self.get_action_managers()

		# if request.user in main_manager.all():
		# 	main_manager.remove(request.user)

		# else:
		# 	main_manager.add(request.user)
		# 	# if the user has previously performed an opposite action, remove that.
		# 	if request.user in opp_manager.all():
		# 		opp_manager.remove(request.user)

		# self.object.save() # so that it would call the object's save method and update the total points
		return Response(status=status.HTTP_200_OK)


class QuestionActionToggleAPIView(ObjectActionToggleAPIView):
	model = Question


class AnswerActionToggleAPIView(ObjectActionToggleAPIView):
	model = Answer


class CommentActionToggleAPIView(ObjectActionToggleAPIView):
	model = Comment


# class QuestionUpvoteToggleAPIView(ObjectActionToggleAPIView):
# 	model = Question
# 	action = 'upvote_toggle'


# class QuestionDownvoteToggleAPIView(ObjectActionToggleAPIView):
# 	model = Question
# 	action = 'downvote_toggle'


# class AnswerUpvoteToggleAPIView(ObjectActionToggleAPIView):
# 	model = Answer
# 	action = 'upvote_toggle'


# class AnswerDownvoteToggleAPIView(ObjectActionToggleAPIView):
# 	model = Answer
# 	action = 'downvote_toggle'


# class CommentUpvoteToggleAPIView(ObjectActionToggleAPIView):
# 	model = Comment
# 	action = 'upvote_toggle'


# class CommentDownvoteToggleAPIView(ObjectActionToggleAPIView):
# 	model = Comment
# 	action = 'downvote_toggle'