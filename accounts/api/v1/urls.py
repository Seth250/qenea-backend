from django.urls import path
from .views import UserCreateAPIView

urlpatterns = [
    # path('signup/', UserCreateAPIView.as_view(), name='signup'),
    path('test/', UserCreateAPIView.as_view(), name='test')
]