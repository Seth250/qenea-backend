from django.urls import include, path

from rest_framework.routers import DefaultRouter

from . import views, viewsets

router = DefaultRouter()
router.register('questions', viewsets.QuestionViewSet, basename='question')
router.register('answers', viewsets.AnswerViewSet, basename='answer')

app_name = 'Questans_API_v1'

urlpatterns = [
    path('', include(router.urls)),
    path('questions/<str:slug>/upvote-toggle/', views.QuestionUpvoteToggleAPIView.as_view(), name='question-upvote-toggle'),
    path('questions/<str:slug>/downvote-toggle/', views.QuestionDownvoteToggleAPIView.as_view(), name='question-downvote-toggle'),
    path('answers/<int:pk>/upvote-toggle/', views.AnswerUpvoteToggleAPIView.as_view(), name='answer-upvote-toggle'),
    path('answers/<int:pk>/downvote-toggle/', views.AnswerDownvoteToggleAPIView.as_view(), name='answer-downvote-toggle')
]
