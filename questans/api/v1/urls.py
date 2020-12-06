from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet, basename='question')
# router.register(r'questions/(?P<slug>[^/.]+)/answers', AnswerViewSet, basename='answer')
router.register(r'answers', views.AnswerViewSet, basename='answer')
router.register(r'comments', views.CommentViewSet, basename='comment')

app_name = 'Questans-API'

urlpatterns = [
    path('', include(router.urls)),
	path('questions/<str:slug>/upvote-toggle/', views.QuestionUpvoteAPIView.as_view(), name='question-upvote-toggle'),
	path('questions/<str:slug>/downvote-toggle/', views.QuestionDownvoteAPIView.as_view(), name='question-downvote-toggle')
]
