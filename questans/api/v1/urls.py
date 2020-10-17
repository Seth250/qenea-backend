from django.urls import path, include
from .views import QuestionViewSet, AnswerViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
router.register(r'questions/(?P<slug>[^/.]+)/answers', AnswerViewSet, basename='answer')

app_name = 'Questions-API'

urlpatterns = [
    path('', include(router.urls))
]