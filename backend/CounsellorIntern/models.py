from django.db import models
from loging.models import CustomUser
from django.utils import timezone
from django.core.validators import RegexValidator,EmailValidator,MaxValueValidator
# from userend.models import Appointment  # Removed to avoid circular import

# # class UserProfile(models.Model):
# #     alpha_validator = RegexValidator(
# #     regex=r'^[a-zA-Z\s-]+$',
# #     message="Only letters, spaces, and hyphens are allowed."
# # )
# #     gender_choices =[("male","male"),("female","female"),("non-binary","non-binary"),("other","other"),("prefer not to say","prefer not to say")]
# #     indian_phone_validator = RegexValidator(
# #     regex=r'^(\+91)?[6-9]\d{9}$',
# #     message="Enter a valid Indian phone number. Either 10 digits or +91 followed by 10 digits.")
# #     fname = models.CharField(max_length=30,validators=[alpha_validator])  
# #     lname = models.CharField(max_length=30,validators=[alpha_validator])
# #     email = models.EmailField(max_length=30,validators=[EmailValidator])

# #     phone_number = models.CharField(validators=[indian_phone_validator],max_length=13)
# #     address = models.TextField(max_length=50)
# #     gender = models.CharField(max_length=18,choices=gender_choices)
# #     DOB = models.DateField()
# #     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
# #     def __str__(self):
# #         return self.user.username
    
# # class UserPrefreference(models.Model):
# #     preferred_date=models.DateField()
# #     id =models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
# #     today_date=models.DateField(default=timezone.now)
# class PendingAppointments(models.Model):
#     time_slot_choices = [("09:00","09:00"),("10:00","10:00"),("11:00","11:00"),("14:00","14:00"),("15:00","15:00"),("16:00","16:00")]
#     doctor_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     patient_id = models.ForeignKey('userend.Appointment', on_delete=models.CASCADE)
#     date = models.DateField()
#     time_slot = models.CharField(max_length=10, choices=time_slot_choices)
#     def __str__(self):
#         return f"{self.doctor.first_name} {self.doctor.last_name}"

class DailyNotification_Counsellor(models.Model):
    time_slot_choices = [("09:00","09:00"),("10:00","10:00"),("11:00","11:00"),("14:00","14:00"),("15:00","15:00"),("16:00","16:00")]
    doctor_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    patient_id = models.ForeignKey('userend.Appointment', on_delete=models.CASCADE)
    date = models.DateField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    time_slot = models.CharField(max_length=10, choices=time_slot_choices)
    def __str__(self):
        return f"{self.doctor.first_name} {self.doctor.last_name}"

class Dailylog_Counserllor_patient(models.Model):
    doctor_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    patient_id = models.ForeignKey('userend.Appointment', on_delete=models.CASCADE)
    date = models.DateField()
    time_slot_choices = [("09:00","09:00"),("10:00","10:00"),("11:00","11:00"),("14:00","14:00"),("15:00","15:00"),("16:00","16:00")]
    time_slot = models.CharField(max_length=10, choices=time_slot_choices)
    completed = models.BooleanField(default=False)
    meeting_link = models.URLField(max_length=500, blank=True, null=True)
    def __str__(self):
        return f"{self.doctor.first_name} {self.doctor.last_name}"

class Psychologist(models.Model):
    indian_phone_validator = RegexValidator(
    regex=r'^(\+91)?[6-9]\d{9}$',
    message="Enter a valid Indian phone number. Either 10 digits or +91 followed by 10 digits.")
    alpha_validator = RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',
    message="Only letters, spaces, and hyphens are allowed.")
    gender_choices =[("male","male"),("female","female")]
    fname=models.CharField(max_length=30,validators=[alpha_validator])
    middle_name=models.CharField(max_length=30,validators=[alpha_validator])
    lname=models.CharField(max_length=30,validators=[alpha_validator])
    email=models.EmailField(max_length=30,validators=[EmailValidator])
    gender=models.CharField(choices=gender_choices, max_length=18)
    phone=models.CharField(max_length=13, validators=[indian_phone_validator])
    DOB=models.DateField()
    address=models.TextField(max_length=50)
    Auth_id=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Dr. {self.fname} {self.lname}"
class DailyLog_Counsellor(models.Model):
    date = models.DateField(default=timezone.localdate)
    created_at = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    present = models.BooleanField(default=False)
    working_day = models.CharField(max_length=12, choices=[('Full','Full'), ('First Half','First Half'), ('Second Half','Second Half')], default='Full')

    class Meta:
        unique_together = ('date', 'doctor')
class AdditionalPsycDetails(models.Model):
    RCI_no=models.CharField(max_length=12)
    Experiance=models.IntegerField(validators=[MaxValueValidator(40)])
    Issue_date_of_license=models.DateField()
    psychologist=models.OneToOneField(Psychologist,on_delete=models.CASCADE,related_name='additional_details')
    
    def __str__(self):
        return f"Details for {self.psychologist.fname} {self.psychologist.lname}"

class InternDetails(models.Model):
    indian_phone_validator = RegexValidator(
    regex=r'^(\+91)?[6-9]\d{9}$',
    message="Enter a valid Indian phone number. Either 10 digits or +91 followed by 10 digits.")
    alpha_validator = RegexValidator(
    regex=r'^[a-zA-Z\s-]+$',
    message="Only letters, spaces, and hyphens are allowed.")
    gender_choices =[("male","male"),("female","female")]
    fname=models.CharField(max_length=30,validators=[alpha_validator])
    middle_name=models.CharField(max_length=30,validators=[alpha_validator])
    lname=models.CharField(max_length=30,validators=[alpha_validator])
    email=models.EmailField(max_length=30,validators=[EmailValidator])
    gender=models.CharField(choices=gender_choices, max_length=18)
    phone=models.CharField(max_length=13, validators=[indian_phone_validator])
    DOB=models.DateField()
    address=models.TextField(max_length=50)
    college_name=models.CharField(max_length=40,validators=[alpha_validator])
    Auth_id=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.fname} {self.lname} - {self.college_name}"

class MeetingSummary(models.Model):
    """
    Model to store AI-generated summaries of counselling sessions
    """
    session = models.OneToOneField(
        Dailylog_Counserllor_patient, 
        on_delete=models.CASCADE,
        related_name='summary'
    )
    transcript = models.TextField(help_text="Full transcript of the meeting")
    summary = models.TextField(help_text="AI-generated summary of the meeting")
    key_points = models.JSONField(
        default=list, 
        help_text="List of key points extracted from the meeting"
    )
    sentiment_analysis = models.JSONField(
        default=dict,
        help_text="Sentiment analysis results"
    )
    recommendations = models.TextField(
        blank=True, 
        help_text="AI-generated recommendations based on the session"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Meeting Summary"
        verbose_name_plural = "Meeting Summaries"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Summary for {self.session.doctor_id.first_name} - {self.session.date}"
