from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.utils import timezone
from .models import JobPostedbyHR, JobAppliedbyUser
from .forms import JobPostedbyHRForm, JobAppliedbyUserForm

# Create your views here.
class JobPostedbyHRView(View):
    """HR Admin view to post new job openings"""
    def get(self, request):
        # Check if user is HR
        if not request.user.is_authenticated or request.user.user_type != 'HR':
            return redirect('loging:loginView')
            
        form = JobPostedbyHRForm()
        # Get all jobs posted by this HR user
        posted_jobs = JobPostedbyHR.objects.filter(job_posted_by=request.user).order_by('-job_posted_date')
        return render(request, 'HRDashbaord/job_posted_by_hr.html', {
            'form': form,
            'posted_jobs': posted_jobs
        })
    
    def post(self, request):
        # Check if user is HR
        if not request.user.is_authenticated or request.user.user_type != 'HR':
            return redirect('loging:loginView')
            
        form = JobPostedbyHRForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.job_posted_by = request.user
            job.save()
            messages.success(request, f'Job "{job.job_title}" has been posted successfully!')
            return redirect('HRDashbaord:post_job')
        else:
            # Debug: Print form errors
            print("Form errors:", form.errors)
            messages.error(request, 'Please fix the errors below and try again.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
        
        posted_jobs = JobPostedbyHR.objects.filter(job_posted_by=request.user).order_by('-job_posted_date')
        return render(request, 'HRDashbaord/job_posted_by_hr.html', {
            'form': form,
            'posted_jobs': posted_jobs
        })

class JobResponsesView(View):
    """HR Admin view to view job responses"""
    def get(self, request):
        # Check if user is HR
        if not request.user.is_authenticated or request.user.user_type != 'HR':
            return redirect('loging:loginView')
        job_responses = JobAppliedbyUser.objects.filter(job_id__job_posted_by=request.user).order_by('-applied_date')
        return render(request, 'HRDashbaord/job_responses.html', {'job_responses': job_responses})

class PastJobs(View):
    """HR Admin view to view past job openings"""
    def get(self, request):
        # Check if user is HR
        if not request.user.is_authenticated or request.user.user_type != 'HR':
            return redirect('loging:loginView')
        
        posted_jobs = JobPostedbyHR.objects.filter(job_posted_by=request.user).order_by('-job_posted_date')
        today = timezone.now().date()
        
        return render(request, 'HRDashbaord/past_jobs.html', {
            'job_responses': posted_jobs,
            'today': today
        })