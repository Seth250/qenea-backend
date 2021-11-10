from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import CommentSerializer


# mixin to add comments route to model viewsets
class ObjectCommentsDetailMixin(object):

    @action(methods=['GET'], detail=True)
    def comments(self, request, *args, **kwargs):
        obj = self.get_object()
        comments = obj.comments.select_related('user')

        page = self.paginate_queryset()
        if page is not None:
            serializer = CommentSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
