# from rest_framework.response import Response
# from rest_framework import mixins
# from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer
from django.contrib.auth import get_user_model


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )
    # authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        return get_user_model().objects.all()


class UserListRetrieveViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_queryset(self):
        return get_user_model().objects.all()
