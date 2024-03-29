from django.urls import path

from . import views

app_name = 'Profiles_API_v1'

urlpatterns = [
    path('profiles/me/', views.ProfileRetrieveUpdateAPIView.as_view(), name='user-profile'),
    path('profiles/<str:username>/', views.ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/follow-toggle/', views.ProfileFollowToggleAPIView.as_view(), name='follow-toggle'),
    path('profiles/<int:pk>/followers/', views.ProfileFollowersListAPIView.as_view(), name='followers-list'),
    path('profiles/<int:pk>/following/', views.ProfileFollowingListAPIView.as_view(), name='following-list')
]
