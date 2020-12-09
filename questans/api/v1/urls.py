from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet, basename='question')
# router.register(r'questions/(?P<slug>[^/.]+)/answers', AnswerVieswSet, basename='answer')
router.register(r'answers', views.AnswerViewSet, basename='answer')
router.register(r'comments', views.CommentViewSet, basename='comment')

app_name = 'Questans-API'

urlpatterns = [
	path('', include(router.urls)),
	path('questions/<str:slug>/<str:action>/', views.QuestionActionToggleAPIView.as_view(), name='question-action-toggle'),
	path('answers/int:pk>/<str:action>/', views.AnswerActionToggleAPIView.as_view(), name='answer-action-toggle'),
	path('comments/<int:pk>/<str:action>/', views.CommentActionToggleAPIView.as_view(), name='comment-action-toggle')
	# path('questions/<str:slug>/upvote-toggle/', views.QuestionUpvoteToggleAPIView.as_view(), name='question-upvote-toggle'),
	# path('questions/<str:slug>/downvote-toggle/', views.QuestionDownvoteToggleAPIView.as_view(), name='question-downvote-toggle'),
	# path('answers/<int:pk>/upvote-toggle/', views.AnswerUpvoteToggleAPIView.as_view(), name='answer-upvote-toggle'),
	# path('answers/<int:pk>/downvote-toggle/', views.AnswerDownvoteToggleAPIView.as_view(), name='answer-downvote-toggle'),
	# path('comments/<int:pk>/upvote-toggle/', views.CommentUpvoteToggleAPIView.as_view(), name='comment-upvote-toggle'),
	# path('comments/<int:pk>/downvote-toggle/', views.CommentDownvoteToggleAPIView.as_view(), name='comment-downvote-toggle')
]
