from django.urls import include, path

from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register('questions', viewsets.QuestionViewSet, basename='question')
router.register('answers', viewsets.AnswerViewSet, basename='answer')

app_name = 'Questans_API_v1'

urlpatterns = [
    path('', include(router.urls))
]
