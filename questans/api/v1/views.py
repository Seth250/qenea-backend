from typing import Literal

from rest_framework import permissions, status, views
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response


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

        # if the user has already performed the main action, then remove it
        if main_manager.filter(pk=user.id).exists():
            main_manager.remove(user)
        else:
            main_manager.add(user)
            # if the user has previously performed an opposite action, then remove that
            if opp_manager.filter(pk=user.id).exists():
                opp_manager.remove(user)

        return Response(status=status.HTTP_204_NO_CONTENT)
