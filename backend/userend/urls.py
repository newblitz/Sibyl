from django.urls import path, reverse_lazy
from . import views
from . import transcription_views
from django.views.generic import TemplateView


app_name="userend"
urlpatterns=[
path("",TemplateView.as_view(template_name="userend/index.html"),name="home"),
# path("register",views.register.as_view(), name="register"),
# path("login", views.login.as_view(), name="login"),
path("know_more",views.know_more,name="know_more"),
path("appointment",views.appointment.as_view(),name="appointment"),
path("appointment/success",views.appointment_success,name="appointment_success"),
# path("create_meet_link",views.create_meet_link,name="create_meet_link"),
path("internship",views.internship.as_view(),name="internship"),
path("apply-job/<int:pk>",views.ApplyJob.as_view(),name="apply_job"),
path('webhooks/daily/', views.daily_webhook_receiver, name='daily_webhook'),
# Meeting analysis API endpoints
path("api/analyze-meeting/", transcription_views.analyze_meeting, name="analyze_meeting"),
path("api/meeting-summary/<int:session_id>/", transcription_views.get_meeting_summary, name="get_meeting_summary"),
# path("counsellor",views.counsellor.as_view(),name="counsellor"),
# path("intern",views.intern.as_view(),name="intern"),
]

