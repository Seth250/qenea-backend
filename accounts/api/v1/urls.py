from django.urls import path
from . import views


app_name = 'accounts_v1'

urlpatterns = [
    path('auth/users/', views.UserCreateAPIView.as_view(), name='signup'),
    path('auth/token/login/', views.ObtainAuthTokenAPIView.as_view(), name='login'),
    path('auth/token/logout/', views.AuthTokenDestroyAPIView.as_view(), name='logout')
]