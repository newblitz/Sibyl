from django import forms
from django.core.validators import RegexValidator,EmailValidator,MinLengthValidator
from .models import CustomUser

class EmailForm(forms.Form):
    """Form for the first step - email verification"""
    email = forms.EmailField(
        max_length=30,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full',
            'placeholder': 'Email Address'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists. Please use a different email or try logging in.')
        return email

class CompleteRegistrationForm(forms.Form):
    """Form for the second step - complete registration after email verification"""
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full',
            'placeholder': 'Username'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full',
            'placeholder': 'Last Name'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full',
            'placeholder': 'Password'
        }),
        validators=[MinLengthValidator(8)]
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full',
            'placeholder': 'Confirm Password'
        }),
        validators=[MinLengthValidator(8)]
    )
    user_type = forms.CharField(max_length=10, initial="Patient", widget=forms.HiddenInput())
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('An account with this username already exists. Please use a different username.')
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Passwords do not match. Please try again.')
        
        return cleaned_data

class OTPVerificationForm(forms.Form):
    """Form for OTP verification"""
    otp = forms.CharField(
        max_length=6,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full',
            'placeholder': 'Enter 6-digit OTP'
        })
    )
    
    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        if not otp.isdigit() or len(otp) != 6:
            raise forms.ValidationError('Please enter a valid 6-digit OTP.')
        return otp