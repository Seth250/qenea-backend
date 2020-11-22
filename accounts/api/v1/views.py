from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserSerializer
from django.contrib.auth import get_user_model


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        return get_user_model().objects.all()


class UserListRetrieveViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )

    def get_queryset(self):
        return get_user_model().objects.all()


class UserLogoutAPIView(APIView):
	permission_classes = (permissions.IsAuthenticated, )

	def post(self, request, *args, **kwargs):
		print(request.user.auth_token)
		return Response(status=status.HTTP_204_NO_CONTENT)