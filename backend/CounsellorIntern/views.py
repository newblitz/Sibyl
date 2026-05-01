from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import DailyLog_CounsellorFormpopup
from .models import DailyLog_Counsellor,DailyNotification_Counsellor


class daily_log_counsellor_popup(LoginRequiredMixin, View):
    def get(self, request):
        form = DailyLog_CounsellorFormpopup()
        return render(request, "CounsellorIntern/daily_log_popup.html", {"form": form})
    
    def post(self, request):
        form = DailyLog_CounsellorFormpopup(request.POST)
        if form.is_valid():
            daily_log = form.save(commit=False)
            daily_log.doctor = request.user
            daily_log.save()
            return redirect('CounsellorIntern:daily_log_success')
        return render(request, "CounsellorIntern/daily_log_popup.html", {"form": form})

def daily_log_success(request):
    return render(request,"CounsellorIntern/daily_log_success.html")

# class Notification_approval(View):
#     def get(self, request):
#         Pending_requests=DailyNotification_Counsellor.objects.filter(doctor_id=request.user.id)
#         return render(request, "CounsellorIntern/notification_approval.html", {"Pending_requests": Pending_requests})
