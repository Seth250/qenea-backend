from rest_framework import permissions, viewsets

from genericsapp.models import Comment
from questans.permissions import IsObjectUserOrReadOnly

from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('user')
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsObjectUserOrReadOnly)

    def list(self, request, *args, **kwargs):
        """
        Endpoint that provides users (unauthenticated or authenticated) with list action for Comment
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Endpoint that provides authenticated users with create action for Comment
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Endpoint that provides users (unauthenticated or authenticated) with retrieve action for Comment
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Endpoint that allows authenticated users to update the Comments they created
        """
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Endpoint that allows authenticated users to delete the Comments they created
        """
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

