from django.urls import path, include
from .views import UserCreateAPIView, UserListRetrieveViewSet
from .token import CustomAuthToken
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('users', UserListRetrieveViewSet, basename='user')

app_name = 'Accounts-API'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', UserCreateAPIView.as_view(), name='user_signup'),
    path('auth/obtain-token/', CustomAuthToken.as_view(), name='api_token_auth')
]