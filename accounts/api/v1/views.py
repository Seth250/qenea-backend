from rest_framework.response import Response
from rest_framework import mixins
# from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )

    def get_queryset(self):
        return get_user_model().objects.all()

    # def create(self, request, *args, **kwargs):
    #     response = super(UserCreateAPIView, self).create(request, *args, **kwargs)
    #     return response


# class UserCreateAPIView(APIView):

#     def post(self, request, *args, **kwargs):
#         serializer = UserSerializer(data=request.data)
#         return Response(serializer.data)



# def post(self, request, format='json'):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         if user:
#             token = Token.objects.create(user=user)
#             json = serializer.data
#             json['token'] = token.key
#             return Response(json, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)