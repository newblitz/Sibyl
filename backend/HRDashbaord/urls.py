from django.urls import path
from . import views

app_name = "HRDashbaord"

urlpatterns = [
    path("post-job/", views.JobPostedbyHRView.as_view(), name="post_job"),
    path("JobResponses/", views.JobResponsesView.as_view(), name="JobResponses"),
    path("PastJobs/", views.PastJobs.as_view(), name="PastJobs"),
]

