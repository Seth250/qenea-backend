from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import AuthTokenSerializer, UserCreateSerializer


User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    """
    Endpoint for unregistered users to create accounts
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserCreateSerializer

    def get_queryset(self):
        return User.objects.all()


class ObtainAuthTokenAPIView(views.APIView):
    """
    Endpoint to obtain authentication token for registered users
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = AuthTokenSerializer

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'auth_token': token.key,
            'email': user.email
        }
        return Response(data=data, status=status.HTTP_200_OK)
