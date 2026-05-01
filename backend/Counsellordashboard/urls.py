from django.urls import path
from . import views

app_name="Counsellordashboard"

urlpatterns=[
    # path("dashboard",views.dashboard,name="dashboard"),
    path("pending_approval",views.Notification_approval.as_view(),name="pending_approval"),
    path("appointments",views.CounsellorAppointments.as_view(),name="appointments"),
]