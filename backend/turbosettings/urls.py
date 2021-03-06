# coding:utf-8
"""turbo-songwriter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from rest_framework_jwt import views as jwt_views

urlpatterns = [
    url(r'^api/admin/', admin.site.urls),
    url(r'^api/', include('songwriter.urls')),
    url(r'^api/account/', include('djoser.urls')),
    url(r'^api/auth/login/', jwt_views.obtain_jwt_token, name='auth'),
    url(r'^api/token-verify/', jwt_views.verify_jwt_token),
    url(r'^api/token-refresh/', jwt_views.refresh_jwt_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns