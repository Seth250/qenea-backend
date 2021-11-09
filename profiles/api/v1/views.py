from rest_framework import generics, permissions, status, views
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from profiles.messages import Messages
from profiles.models import Profile

from .serializers import ProfileFollowSerializer, ProfileSerializer


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """
    Endpoint to view the profile information of users
    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = ProfileSerializer

    def get_object(self):
        username = self.kwargs['username']
        try:
            profile = Profile.objects.select_related('user').get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound('Oops! Looks like there is no user with that username')

        return profile


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Endpoint for logged in users to view and update their profile information
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProfileSerializer

    def get_object(self):
        return Profile.objects.select_related('user').get(user=self.request.user)


class ProfileFollowToggleAPIView(views.APIView):
    """
    Endpoint for logged in users to follow/unfollow other users
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, pk):
        try:
            obj = Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise NotFound(Messages.PROFILE_NOT_FOUND_ERROR)

        return obj

    def post(self, request, *args, **kwargs):
        following = True
        user_profile = request.user.profile
        obj = self.get_object(pk=kwargs.get('pk'))
        # if the user is already being followed, then unfollow
        if user_profile.following.filter(pk=obj.pk).exists():
            user_profile.following.remove(obj)
            following = False
        # else follow
        else:
            user_profile.following.add(obj)

        return Response(data={'following': following}, status=status.HTTP_200_OK)


class ProfileFollowersListAPIView(generics.ListAPIView):
    """
    Endpoint for logged in users to list the followers of a user
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProfileFollowSerializer 


    def get_queryset(self):
        pk_ = self.kwargs['pk']
        try:
            profile = Profile.objects.get(pk=pk_)
        except Profile.DoesNotExist:
            raise NotFound(Messages.PROFILE_NOT_FOUND_ERROR)

        return profile.followers.select_related('user')


class ProfileFollowingListAPIView(generics.ListAPIView):
    """
    Endpoint for logged in users to view the following-list of a user
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ProfileFollowSerializer 


    def get_queryset(self):
        pk_ = self.kwargs['pk']
        try:
            profile = Profile.objects.get(pk=pk_)
        except Profile.DoesNotExist:
            raise NotFound(Messages.PROFILE_NOT_FOUND_ERROR)

        return profile.following.select_related('user')
