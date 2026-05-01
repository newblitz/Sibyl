from django.urls import path
from . import views

app_name="Internordashboard"

urlpatterns=[
path("genz-dashboard",views.genz_dashboard,name="genz_dashboard"),
]