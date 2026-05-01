# from django.db import models
# from loging.models import CustomUser
# from django.utils import timezone
# from django.core.validators import RegexValidator,EmailValidator,MaxValueValidator

# # Create your models here.

# from django.db import models


# class UserProfile(models.Model):
#     alpha_validator = RegexValidator(
#     regex=r'^[a-zA-Z\s-]+$',
#     message="Only letters, spaces, and hyphens are allowed."
# )
#     gender_choices =[("male","male"),("female","female"),("non-binary","non-binary"),("other","other"),("prefer not to say","prefer not to say")]
#     indian_phone_validator = RegexValidator(
#     regex=r'^(\+91)?[6-9]\d{9}$',
#     message="Enter a valid Indian phone number. Either 10 digits or +91 followed by 10 digits.")
#     fname = models.CharField(max_length=30,validators=[alpha_validator])  
#     lname = models.CharField(max_length=30,validators=[alpha_validator])
#     email = models.EmailField(max_length=30,validators=[EmailValidator])

#     phone_number = models.CharField(validators=[indian_phone_validator],max_length=13)
#     # address = models.TextField(max_length=50)
#     gender = models.CharField(max_length=18,choices=gender_choices)
#     DOB = models.DateField()
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     def __str__(self):
#         return self.user.username
    
# class UserPrefreference(models.Model):
#     preferred_date=models.DateField()
#     id =models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
#     today_date=models.DateField(default=timezone.now)
    
# class Psychologist(models.Model):
#     indian_phone_validator = RegexValidator(
#     regex=r'^(\+91)?[6-9]\d{9}$',
#     message="Enter a valid Indian phone number. Either 10 digits or +91 followed by 10 digits.")
#     alpha_validator = RegexValidator(
#     regex=r'^[a-zA-Z\s-]+$',
#     message="Only letters, spaces, and hyphens are allowed."
# )
#     gender_choices =[("male","male"),("female","female")]
#     fname=models.CharField(max_length=30,validators=[alpha_validator])
#     middle_name=models.CharField(max_length=30,validators=[alpha_validator],null=True)
#     lname=models.CharField(max_length=30,validators=[alpha_validator])
#     email=models.EmailField(max_length=30,validators=[EmailValidator])
#     gender=models.CharField(choices=gender_choices, max_length=18)
#     phone=models.CharField(max_length=13, validators=[indian_phone_validator])
#     DOB=models.DateField()
#     address=models.TextField(max_length=50)
#     id=models.AutoField(primary_key=True)

# class AdditionalPsycDetails(models.Model):
#     RCI_no=models.CharField(max_length=12)
#     Experiance=models.IntegerField(validators=[MaxValueValidator(40)])
#     Issue_date_of_license=models.DateField()
#     id=models.OneToOneField(Psychologist,on_delete=models.CASCADE,primary_key=True)


# class DailyLog(models.Model):
#     date = models.DateField()
#     doctor = models.OneToOneField(Psychologist,on_delete=models.CASCADE)
#     present = models.BooleanField(max_length=3,choices=[("y","yes"),("n","no")])
#     working_day = models.CharField(max_length=10, choices=[('Full','Full'), ('Half','Half')])

#     class Meta:
#         unique_together = ('date', 'doctor')

# class InternDetails(models.Model):
#     indian_phone_validator = RegexValidator(
#     regex=r'^(\+91)?[6-9]\d{9}$',
#     message="Enter a valid Indian phone number. Either 10 digits or +91 followed by 10 digits.")
#     alpha_validator = RegexValidator(
#     regex=r'^[a-zA-Z\s-]+$',
#     message="Only letters, spaces, and hyphens are allowed.")
#     gender_choices =[("male","male"),("female","female")]
#     fname=models.CharField(max_length=30,validators=[alpha_validator])
#     middle_name=models.CharField(max_length=30,validators=[alpha_validator])
#     lname=models.CharField(max_length=30,validators=[alpha_validator])
#     email=models.EmailField(max_length=30,validators=[EmailValidator])
#     gender=models.CharField(choices=gender_choices, max_length=18)
#     phone=models.CharField(max_length=13, validators=[indian_phone_validator])
#     DOB=models.DateField()
#     address=models.TextField(max_length=50)
#     college_name=models.CharField(max_length=40,validators=[alpha_validator])
