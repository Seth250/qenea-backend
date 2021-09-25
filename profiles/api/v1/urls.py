from django.urls import path
from . import views


app_name = 'Profiles_API_v1'

urlpatterns = [
    path('profiles/me/', views.ProfileRetrieveUpdateAPIView.as_view()),
    path('profiles/<str:username>/', views.ProfileDetailAPIView.as_view())
]