from rest_framework import generics, permissions

from profiles.models import Profile

from .serializers import ProfileSerializer


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """
    Endpoint to view the profile information of users
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = ProfileSerializer

    def get_object(self):
        username = self.kwargs['username']
        return Profile.objects.get(user__username=username)


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Endpoint for current logged in users to view and update their profile information
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
