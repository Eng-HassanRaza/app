"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.conf import settings

from web.views import auth_view

admin.site.site_title = 'LEAN! 管理サイト'
admin.site.site_header = 'LEAN! 管理サイト'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/social/login/cancelled/', auth_view.canceled, name="socialaccount_login_cancelled"),
    path('accounts/social/login/error/', auth_view.error, name="error"),
    path('accounts/', include('allauth.urls')),
    path('', include("web.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,
document_root=settings.STATIC_ROOT)
