from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator,RegexValidator
from django.utils import timezone
from loging.models import CustomUser

# Create your models here.
class JobPostedbyHR(models.Model):
    job_type_choices = [("Counsellor", "Counsellor"),("Intern", "Intern")]
    job_location_choices = [("Remote", "Remote"),("On-site", "On-site")]
    job_title = models.CharField(max_length=100)
    job_description = models.TextField()
    job_location = models.CharField(max_length=100, choices=job_location_choices)
    job_type = models.CharField(max_length=100, choices=job_type_choices)
    job_salary = models.DecimalField(max_digits=10, decimal_places=2)
    job_posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    job_posted_date = models.DateTimeField(auto_now_add=True)
    job_duration = models.IntegerField(validators=[MinValueValidator(1)])
    job_experience = models.IntegerField(validators=[MinValueValidator(0)])
    last_date_to_apply = models.DateField()

    def __str__(self):
        return self.job_title
    
    @property
    def job_applied_count(self):
        return self.jobappliedbyuser_set.count()

class JobAppliedbyUser(models.Model):
    job_id = models.ForeignKey(JobPostedbyHR, on_delete=models.CASCADE)
    age = models.IntegerField(validators=[MinValueValidator(18),MaxValueValidator(60)])
    gender = models.CharField(max_length=100, choices=[("male", "male"),("female", "female")])
    email = models.EmailField(max_length=100)
    first_name = models.CharField(max_length=100,validators=[RegexValidator(regex=r'^[a-zA-Z\s-]+$',message="Only letters, spaces, and hyphens are allowed.")])
    last_name = models.CharField(max_length=100,validators=[RegexValidator(regex=r'^[a-zA-Z\s-]+$',message="Only letters, spaces, and hyphens are allowed.")])
    address = models.TextField()
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.FileField(upload_to="cover_letters/")
    applied_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_id.job_title}"
    