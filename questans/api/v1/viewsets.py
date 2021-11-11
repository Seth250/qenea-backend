from rest_framework import permissions, viewsets

from comments.api.v1.mixins import ObjectCommentsViewSetMixin
from questans.models import Question
from questans.permissions import IsObjectUserOrReadOnly

from .serializers import QuestionSerializer


class QuestionViewSet(ObjectCommentsViewSetMixin, viewsets.ModelViewSet):
    queryset = Question.objects.select_related('user')
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsObjectUserOrReadOnly)
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        """
        Endpoint that provides users (unauthenticated or authenticated) with list action for Question
        """
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
        Endpoint that allows authenticated users to delete Questions they created
        """
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
