from typing import Literal

from rest_framework import generics, permissions, status, views
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import APIException, NotFound, PermissionDenied
from rest_framework.response import Response

from questans.api.v1.serializers import AnswerSerializer
from questans.models import Answer, Question


class BaseObjectActionToggleAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    model = None
    lookup_field: Literal['pk', 'slug'] = 'pk'
    action: Literal['upvote-toggle', 'downvote-toggle']

    def get_object(self):
        try:
            lookup_kwarg = {self.lookup_field: self.kwargs.get(self.lookup_field)}
            instance = self.model.objects.get(**lookup_kwarg)
        except:
            raise NotFound('The requested object does not exist.')

        return instance

    def get_object_action_managers(self):
        obj = self.get_object()
        if self.action == 'upvote-toggle':
            return obj.upvotes, obj.downvotes

        elif self.action == 'downvote-toggle':
            return obj.downvotes, obj.upvotes

        raise APIException

    def post(self, request, *args, **kwargs):
        main_manager, opp_manager = self.get_object_action_managers()
        user = request.user

        # if the user has already performed this main action, then remove it
        if main_manager.filter(pk=user.id).exists():
            main_manager.remove(user)
        else:
            main_manager.add(user)
            # if the user has previously performed an opposite action, then remove that
            if opp_manager.filter(pk=user.id).exists():
                opp_manager.remove(user)

        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionUpvoteToggleAPIView(BaseObjectActionToggleAPIView):
    """
    Endpoint for logged in users to add/remove their upvotes to questions
    """
    model = Question
    lookup_field = 'slug'
    action = 'upvote-toggle'


class QuestionDownvoteToggleAPIView(BaseObjectActionToggleAPIView):
    """
    Endpoint for logged in users to add/remove their downvotes to questions
    """
    model = Question
    lookup_field = 'slug'
    action = 'downvote-toggle'


class AnswerUpvoteToggleAPIView(BaseObjectActionToggleAPIView):
    """
    Endpoint for logged in users to add/remove their upvotes to answers
    """
    model = Answer
    action = 'upvote-toggle'


class AnswerDownvoteToggleAPIView(BaseObjectActionToggleAPIView):
    """
    Endpoint for logged in users to add/remove their downvotes to answers
    """
    model = Answer
    action = 'downvote-toggle'


class QuestionAnswersListAPIView(generics.ListAPIView):
    """
    Endpoint that provides users (unauthenticated or authenticated) with list action for a question's answers
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = AnswerSerializer

    def get_queryset(self):
        try:
            question = Question.objects.get(slug=self.kwargs['slug'])
        except:
            raise NotFound('question does not exist')

        return Answer.objects.select_related('question', 'user').filter(question=question)


class AnswerAcceptToggleAPIView(views.APIView):
    """
    Endpoint for the question owner to accept or un-accept an answer
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        try:
            instance = Answer.objects.get(pk=self.kwargs['pk'])
        except:
            raise NotFound('answer does not exist.')

        return instance

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        question = obj.question
        # if the question owner is not the same as the current logged in user
        if question.user != request.user:
            raise PermissionDenied

        qs = question.answers.exclude(pk=obj.pk).filter(is_accepted=True)
        if qs.exists():
            prev_accepted_answer = qs.first()
            prev_accepted_answer.is_accepted = False
            prev_accepted_answer.save()

        obj.is_accepted = not obj.is_accepted
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
