from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer


User = get_user_model()

class UserCreateAPIView(generics.CreateAPIView):
    """
    Endpoint for unregistered users to create accounts
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserCreateSerializer

    def get_queryset(self):
        return User.objects.all()
