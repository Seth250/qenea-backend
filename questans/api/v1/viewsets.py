from rest_framework import permissions, viewsets

from comments.api.v1.mixins import ObjectCommentsViewSetMixin
from questans.models import Answer, Question
from questans.permissions import IsObjectUserOrReadOnly

from .serializers import (AnswerSerializer, QuestionListSerializer,
                          QuestionSerializer)


class QuestionViewSet(ObjectCommentsViewSetMixin, viewsets.ModelViewSet):
    queryset = Question.objects.select_related('user')
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsObjectUserOrReadOnly)
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        """
        Endpoint that provides users (unauthenticated or authenticated) with list action for Question
        """
        self.serializer_class = QuestionListSerializer
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Endpoint that provides authenticated users with create action for Question
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Endpoint that provides users (unauthenticated or authenticated) with retrieve action for Question
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Endpoint that allows authenticated users to update the Questions they created
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Endpoint that allows authenticated users to delete the Questions they created
        """
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class AnswerViewSet(ObjectCommentsViewSetMixin, viewsets.ModelViewSet):
    queryset = Answer.objects.select_related('user', 'question')
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsObjectUserOrReadOnly)

    def list(self, request, *args, **kwargs):
        """
        Endpoint that provides users (unauthenticated or authenticated) with list action for Answer
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Endpoint that provides authenticated users with create action for Answer
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Endpoint that provides users (unauthenticated or authenticated) with retrieve action for Answer
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Endpoint that allows authenticated users to update the Answers they created
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Endpoint that allows authenticated users to delete the Answers they created
        """
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
