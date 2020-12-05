from django.urls import path, include
from .views import QuestionViewSet, AnswerViewSet, CommentViewSet, QuestionUpvoteView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')
# router.register(r'questions/(?P<slug>[^/.]+)/answers', AnswerViewSet, basename='answer')
router.register(r'answers', AnswerViewSet, basename='answer')
router.register(r'comments', CommentViewSet, basename='comment')

app_name = 'Questans-API'

urlpatterns = [
    path('', include(router.urls)),
	path('questions/<str:slug>/upvote-toggle/', QuestionUpvoteView.as_view(), name='question-upvote-toggle')
]
