from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator,EmailValidator

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        if not first_name:
            raise ValueError('The First Name field must be set')
        if not last_name:
            raise ValueError('The Last Name field must be set')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'Counsellor')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, first_name, last_name, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPES = [
        ("Counsellor", "Counsellor"),
        ("patient", "Patient"),
        ("intern", "intern"),
        ("HR", "HR"),
    ]
    email = models.EmailField(max_length=30,validators=[EmailValidator],unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES,default="Patient")
    email_verified = models.BooleanField(default=False)
    # phone_number = models.CharField(
    #     max_length=13, 
    #     validators=[RegexValidator(
    #         regex=r'^(\+91)?[6-9]\d{9}$',
    #         message="Enter a valid Indian phone number. Either 10 digits or +91 followed by 10 digits."
    #     )],
    #     unique=True
    # )
    # # email = models.EmailField(blank=True, null=True)  # Make email optional
    USERNAME_FIELD = "username"  # Use username for authentication
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email+" "+self.user_type


class EmailVerification(models.Model):
    email = models.EmailField(max_length=30, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Email Verification"
        verbose_name_plural = "Email Verifications"
    
    def __str__(self):
        return f"{self.email} - {self.otp}"