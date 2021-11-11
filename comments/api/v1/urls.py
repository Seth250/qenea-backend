from django.urls import include, path

from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register('comments', viewsets.CommentViewSet, basename='comment')

app_name = 'Comments_API_v1'

urlpatterns = [
    path('', include(router.urls))
]
