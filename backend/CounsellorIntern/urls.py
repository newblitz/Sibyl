from django.urls import path
from . import views

app_name = 'CounsellorIntern'

urlpatterns = [
    path('daily-log/', views.daily_log_counsellor_popup.as_view(), name='daily_log_popup'),
    path('daily-log/success/', views.daily_log_success, name='daily_log_success'),
]