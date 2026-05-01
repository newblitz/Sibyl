from django import forms
from django.core.validators import MinValueValidator
from django.utils import timezone
from .models import JobPostedbyHR, JobAppliedbyUser

class JobPostedbyHRForm(forms.ModelForm):
    class Meta:
        model = JobPostedbyHR
        fields = ['job_title', 'job_description', 'job_location', 'job_type', 'job_salary', 'job_duration', 'job_experience', 'last_date_to_apply']
        widgets = {
            'last_date_to_apply': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'job_salary': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
            'job_duration': forms.NumberInput(attrs={'min': '1', 'step': '1'}),
            'job_experience': forms.NumberInput(attrs={'min': '0', 'step': '1'}),
        }
    
    def clean_job_salary(self):
        salary = self.cleaned_data.get('job_salary')
        if salary is not None and salary < 0:
            raise forms.ValidationError("Salary cannot be negative.")
        return salary
    
    def clean_job_duration(self):
        duration = self.cleaned_data.get('job_duration')
        if duration is not None and duration < 1:
            raise forms.ValidationError("Job duration must be at least 1 month.")
        return duration
    
    def clean_job_experience(self):
        experience = self.cleaned_data.get('job_experience')
        if experience is not None and experience < 0:
            raise forms.ValidationError("Experience cannot be negative.")
        return experience
    
    def clean_last_date_to_apply(self):
        last_date = self.cleaned_data.get('last_date_to_apply')
        if last_date and last_date <= timezone.now().date():
            raise forms.ValidationError("Last date to apply must be in the future.")
        return last_date

class JobAppliedbyUserForm(forms.ModelForm):
    class Meta:
        model = JobAppliedbyUser
        fields = ['age', 'gender', 'email', 'first_name', 'last_name', 'address', 'resume', 'cover_letter']
        widgets = {
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.FileInput(attrs={'class': 'form-control'}),
        }
