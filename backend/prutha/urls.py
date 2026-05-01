"""
URL configuration for prutha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("userend.urls", namespace="userend")),
    # path("register/", include("registeruser.urls", namespace="registeruser")),
    path("create/", include("loging.urls",namespace="loging")),
    path("counsellor/", include("CounsellorIntern.urls", namespace="CounsellorIntern")),
    path("counsellor-dashboard/", include("Counsellordashboard.urls", namespace="Counsellordashboard")),
    path("hr/", include("HRDashbaord.urls", namespace="HRDashbaord")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        # Handle old resume path for backward compatibility
        re_path(r'^resumes/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'resumes')}),
    ]
