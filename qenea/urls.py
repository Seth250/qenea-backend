"""qenea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from drf_yasg2.views import get_schema_view
from drf_yasg2 import openapi
from django.conf.urls import url
from django.conf import settings
from rest_framework import permissions
from django.conf.urls.static import static


schema_view = get_schema_view(
	openapi.Info(
		title="Qenea API Documentation",
		default_version='v1',
		description='Official Documentation for Qenea API'
	),
	public=True,
	permission_classes=(permissions.AllowAny, )
)

urlpatterns = [
    path('admin/', admin.site.urls),

	url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

	url(r'^api-auth/', include('rest_framework.urls')),

    path('', include('accounts.api.v1.urls')),
    path('', include('questans.api.v1.urls')),
	path('', include('profiles.api.v1.urls')),
	# path('auth/reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# the media url will only be added when DEBUG is True because static() returns an empty list when DEBUG is False
