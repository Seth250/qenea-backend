from django.urls import path, include
from .views import UserCreateAPIView, UserListRetrieveViewSet, UserLogoutAPIView
from .token import CustomAuthToken
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users', UserListRetrieveViewSet, basename='user')

app_name = 'Accounts-API'

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', UserCreateAPIView.as_view(), name='user-signup'),
    path('auth/token/login/', CustomAuthToken.as_view(), name='user-auth-token'),
	path('auth/token/logout/', UserLogoutAPIView.as_view(), name='user-logout')
]