from django.db import models
from django.core.validators import RegexValidator,EmailValidator
from loging.models import CustomUser
from django.utils import timezone
# from CounsellorIntern.models import DailyLog_Counsellor
# from CounsellorIntern.models import Psychologist  # Removed to avoid circular import
# from django.contrib.auth.models import User
class Appointment(models.Model):
    @staticmethod
    def get_doctor_choices():
        """Get list of counsellor choices for forms"""
        doctors = CustomUser.objects.filter(user_type="Counsellor")
        choices = []
        for doctor in doctors:
            name = f"{doctor.first_name} {doctor.last_name}"
            choices.append((doctor.id, name))
        return choices

    # @staticmethod
    # def get_intern_choices():
    #     """Get list of intern choices for forms"""
    #     interns = CustomUser.objects.filter(user_type="intern")
    #     choices = []
    #     for intern in interns:
    #         name = f"{intern.first_name} {intern.last_name}"
    #         choices.append((intern.id, name))
    #     return choices
    
    meet_link = models.URLField(max_length=500, blank=True, null=True)
    audio_recording = models.FileField(upload_to='recordings/', blank=True, null=True)# Doctor_choices = get_doctor_choices()  # Removed to avoid database access during import
    gender=[("male","Male"),("female",'Female'),("Prefer not to say","Prefer not to say"),("others","others")]
    time_slot_choices = [("09:00","09:00"),("10:00","10:00"),("11:00","11:00"),("14:00","14:00"),("15:00","15:00"),("16:00","16:00")]
    duration_choices = [("30","30"),("45","45"),("60","60"),("90","90")]
    session_type_choices = [("individual","individual"),("couples","couples"),("family","family"),("group","group")]
    first_name = models.CharField(max_length=100,validators=[RegexValidator(regex=r'^[a-zA-Z\s-]+$',message="Only letters, spaces, and hyphens are allowed.")])
    room_name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    last_name = models.CharField(max_length=100,validators=[RegexValidator(regex=r'^[a-zA-Z\s-]+$',message="Only letters, spaces, and hyphens are allowed.")])
    # email = models.EmailField(max_length=100,validators=[EmailValidator])
    # phone = models.CharField(max_length=100,validators=[RegexValidator(regex=r'^(\+91)?[6-9]\d{9}$',message="Enter a valid Indian phone number. Either 10 digits or +91 followed by 10 digits.")])
    appointment_date = models.DateField()
    # created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    time_slot = models.CharField(max_length=10, choices=time_slot_choices)
    duration = models.CharField(max_length=10, choices=duration_choices)
    session_type = models.CharField(max_length=20, choices=session_type_choices)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    gender=models.CharField(max_length=20,choices=gender,null=True)
    IsPending = models.BooleanField(default=True)
    # meet_link = models.URLField(max_length=500, blank=True, null=True, help_text="Google Meet link for the appointment")
    # meet_link_type = models.CharField(max_length=20, choices=[('genuine', 'Genuine Google Meet')], default='genuine', help_text="Type of meet link generated - only genuine Google Meet links are allowed")
    selected_doctor = models.ForeignKey('CounsellorIntern.Psychologist', on_delete=models.CASCADE, related_name='appointments_as_doctor')
    Assigned_doctor = models.ForeignKey('CounsellorIntern.Psychologist', on_delete=models.CASCADE, related_name='appointments_as_assigned_doctor', null=True, blank=True)
    # selected_intern = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments_as_intern', null=True, blank=True, limit_choices_to={'user_type': 'intern'})
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
# class ClientProfile(models.Model):
#     class Gender(models.TextChoices):
#         MALE = "male", "Male"
#         FEMALE = "female", "Female"
#         NON_BINARY = "non-binary", "Non-binary"
#         UNSPECIFIED = "unspecified", "Prefer not to say"

#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     age = models.PositiveIntegerField(null=True, blank=False)
#     phone = models.CharField(max_length=10, blank=False)
#     gender = models.CharField(max_length=20, choices=Gender.choices, default=Gender.UNSPECIFIED)
#     emergency_contact = models.CharField(max_length=20, blank=True)
#     medical_history = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Client: {self.user.get_full_name() or self.user.username}"


# class TherapistProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     bio = models.TextField(blank=True)
#     qualifications = models.CharField(max_length=255, blank=True)
#     years_experience = models.PositiveIntegerField(default=0)
#     license_number = models.CharField(max_length=50, blank=True)
#     rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
#     photo_url = models.URLField(blank=True)
#     # hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Therapist: {self.user.get_full_name() or self.user.username}"

# class DailyLog_Counsellor(models.Model):
#     date = models.DateField()
#     doctor = models.OneToOneField(Psychologist,on_delete=models.CASCADE)
#     present = models.BooleanField(max_length=3,choices=[("y","yes"),("n","no")])
#     working_day = models.CharField(max_length=10, choices=[('Full','Full'), ('Half','Half')])

#     class Meta:
#         unique_together = ('date', 'doctor')





# class AvailabilitySlot(models.Model):
#     therapist = models.ForeignKey(TherapistProfile, on_delete=models.CASCADE, related_name='availability')
#     start = models.DateTimeField()
#     end = models.DateTimeField()
#     is_available = models.BooleanField(default=True)

#     class Meta:
#         constraints = [
#             models.CheckConstraint(check=models.Q(end__gt=models.F("start")), name="availability_end_after_start"),
#         ]

#     def __str__(self):
#         return f"{self.therapist.user.username}: {self.start} - {self.end}"


# class Appointment(models.Model):
#     class Status(models.TextChoices):
#         PENDING = "pending", "Pending"
#         CONFIRMED = "confirmed", "Confirmed"
#         COMPLETED = "completed", "Completed"
#         CANCELED = "canceled", "Canceled"

#     client_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_appointments')
#     therapist_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='therapist_appointments')
#     scheduled_for = models.DateTimeField()
#     reason = models.CharField(max_length=200, blank=True)
#     status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
#     notes = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         indexes = [models.Index(fields=["scheduled_for", "status"])]

#     def __str__(self):
#         return f"{self.client_user.username} → {self.therapist_user.username} on {self.scheduled_for}"


# class Review(models.Model):
#     appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='review')
#     rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # 1–5
#     comment = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Review for {self.appointment} - {self.rating} stars"


# class Initiative(models.Model):
#     title = models.CharField(max_length=150)
#     summary = models.CharField(max_length=300, blank=True)
#     content = models.TextField(blank=True)
#     image_url = models.URLField(blank=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


# class InternshipPosting(models.Model):
#     class Type(models.TextChoices):
#         INTERNSHIP = "internship", "Internship"
#         JOB = "job", "Job"

#     title = models.CharField(max_length=150)
#     kind = models.CharField(max_length=20, choices=Type.choices, default=Type.INTERNSHIP)
#     location = models.CharField(max_length=120, blank=True)
#     stipend = models.CharField(max_length=80, blank=True)
#     description = models.TextField()
#     requirements = models.TextField(blank=True)
#     deadline = models.DateField(null=True, blank=True)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title


# class InternshipApplication(models.Model):
#     class Status(models.TextChoices):
#         SUBMITTED = "submitted", "Submitted"
#         REVIEW = "in_review", "In review"
#         ACCEPTED = "accepted", "Accepted"
#         REJECTED = "rejected", "Rejected"

#     posting = models.ForeignKey(InternshipPosting, on_delete=models.CASCADE, related_name='applications')
#     applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='internship_applications')
#     cover_letter = models.TextField(blank=True)
#     resume_url = models.URLField(blank=True)
#     status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ("posting", "applicant")

#     def __str__(self):
#         return f"{self.applicant.username} - {self.posting.title}"

# class Therapist(models.Model):
#     first_name=models.charfield(max_length=20)
#     last_name=models.charfield(max_lenghth=20)
#     email=models.EmailField(max_length=20)
#     password=models.CharField(widget=models.PasswordInput)
#     confirm_password=models.CharField(widget=models.PasswordInput)

