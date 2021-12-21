"""qenea_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='Qenea API Documentation',
        default_version='v1',
        description='Qenea (pronounced Q and A) is a question and answer application',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='ayowaleakintayo@gmail.com'),
        license=openapi.License(name='MIT License')
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser, )
)

v1_urls = [
    path('', include('accounts.api.v1.urls')),
    path('', include('comments.api.v1.urls')),
    path('', include('profiles.api.v1.urls')),
    path('', include('questans.api.v1.urls'))
]

urlpatterns = [
    path('qa-admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api/v1/', include(v1_urls))
]
