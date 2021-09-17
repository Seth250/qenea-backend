from django.urls import path
from . import views


urlpatterns = [
    path('auth/users/', views.UserCreateAPIView.as_view(), name='signup')
]