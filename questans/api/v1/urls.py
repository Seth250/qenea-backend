from django.urls import path, include
from .views import QuestionViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('questions', QuestionViewSet, basename='question')

app_name = 'Questions-API'

urlpatterns = [
    path('', include(router.urls))
]