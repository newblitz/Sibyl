import os
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.contrib.auth import views as auth_views

app_name = "loging"

urlpatterns = [
    path("", views.CreateAccount.as_view(), name="CreateAccount"),
    path("verify-otp/", views.VerifyOTP.as_view(), name="verify_otp"),
    path("complete-registration/", views.CompleteRegistration.as_view(), name="complete_registration"),
    path("login/", views.CustomLoginView.as_view(), name="loginView"),
    path("logout/", views.logout_view, name="logout"),
    # path('logout/', auth_views.LogoutView.as_view(next_page='loging/logout.html'), name='logout'),
    path("redirect/", views.redirect_view.as_view(), name="redirect"),
    path("counsellor/", views.counsellor.as_view(), name="counsellor"),
    path("intern/", views.intern.as_view(), name="intern"),
    path("hr/", views.hr.as_view(), name="hr_dashboard"),
    # path("how-it-works/", views.how_it_works, name="how-it-works"),
    # path("list-psychologists/", views.list_psychologists, name="list-psychologists"),
]