from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

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
    Endpoint for logged in users to view and update their profile information
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class FollowToggleProfileAPIView(views.APIView):
    """
    Endpoint for logged in users to follow/unfollow other users
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, username):
        try:
            return Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        following = True
        user_profile = request.user.profile
        obj = self.get_object(username=kwargs.get('username'))
        # if the user is already being followed, then unfollow
        if user_profile.following.filter(pk=obj.pk).exists():
            user_profile.following.remove(obj)
            following = False
        # else follow
        else:
            user_profile.following.add(obj)

        return Response(data={'following': following}, status=status.HTTP_200_OK)
