from django.urls import path
from .views import UserCreateAPIView


app_name = 'Accounts-API'

urlpatterns = [
    path('signup/', UserCreateAPIView.as_view(), name='user_signup')
]