"""tickets URL Configuration

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
from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from backend import views as core_views

from django.contrib.auth.views import LoginView as login
from django.views.generic.list import ListView
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tickets import settings
from rest_framework import routers, serializers, viewsets
import backend.views as views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^api/', include('backend.urls')),
    url(r'^login/$', login.as_view(), {'template_name': 'login.html'}, name='login'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^logout/$', core_views.my_logout, name='logout'),
    path('auth/jwt/create/', views.CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
