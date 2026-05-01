from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import IntegrityError
from .forms import EmailForm, CompleteRegistrationForm, OTPVerificationForm
from .models import CustomUser, EmailVerification
from .email_service import email_service
from CounsellorIntern.models import DailyLog_Counsellor, Dailylog_Counserllor_patient
from HRDashbaord.models import JobPostedbyHR, JobAppliedbyUser
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


# Create your views here.

# views.py
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

@method_decorator(never_cache, name='dispatch')
class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'  # your login template

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # redirect to home/dashboard if already logged in
        return super().dispatch(request, *args, **kwargs)

class CreateAccount(View):
    """First step: Email verification"""
    
    @staticmethod
    def generate_otp():
        return random.randint(100000, 999999)

    @staticmethod
    def send_verification_email(email, otp):
        """Send verification email using SendGrid"""
        return email_service.send_verification_email(email, otp)

    def get(self, request):
        form = EmailForm()
        return render(request, "loging/registerwith.html", {"form": form})
    
    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = self.generate_otp()
            
            # Delete any existing verification for this email
            EmailVerification.objects.filter(email=email).delete()
            
            # Create new verification record
            verification = EmailVerification.objects.create(
                email=email,
                otp=str(otp)
            )
            
            # Send OTP email
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, 'An account with this email already exists. Please use a different email or try logging in.')
                return render(request, "loging/registerwith.html", {"form": form})
            else:
                print(f"DEBUG: Attempting to send OTP {otp} to {email}")
                email_sent = self.send_verification_email(email, otp)
                print(f"DEBUG: Email sending result: {email_sent}")
            
            if email_sent:
                messages.success(request, f'Verification code sent to {email}')
                # Store email in session for next step
                request.session['registration_email'] = email
                return redirect('loging:verify_otp')
            else:
                messages.error(request, 'Failed to send verification email. Please try again.')
                return render(request, "loging/registerwith.html", {"form": form})
        else:
            # Display form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return render(request, "loging/registerwith.html", {"form": form})


class VerifyOTP(View):
    """Second step: OTP verification"""
    
    def get(self, request):
        email = request.session.get('registration_email')
        if not email:
            messages.error(request, 'Please start the registration process again.')
            return redirect('loging:CreateAccount')
        
        form = OTPVerificationForm()
        return render(request, "loging/otp_verification.html", {"form": form, "email": email})
    
    def post(self, request):
        email = request.session.get('registration_email')
        if not email:
            messages.error(request, 'Please start the registration process again.')
            return redirect('loging:CreateAccount')
        
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            
            try:
                verification = EmailVerification.objects.get(email=email, otp=otp)
                
                # Check if OTP is not expired (5 minutes)
                if timezone.now() - verification.created_at > timedelta(minutes=5):
                    messages.error(request, 'OTP has expired. Please request a new one.')
                    return redirect('loging:CreateAccount')
                
                # Check attempts
                if verification.attempts >= 3:
                    messages.error(request, 'Too many failed attempts. Please start registration again.')
                    verification.delete()
                    return redirect('loging:CreateAccount')
                
                # Mark as verified
                verification.is_verified = True
                verification.save()
                
                messages.success(request, 'Email verified successfully!')
                return redirect('loging:complete_registration')
                
            except EmailVerification.DoesNotExist:
                # Increment attempts
                try:
                    verification = EmailVerification.objects.get(email=email)
                    verification.attempts += 1
                    verification.save()
                    
                    if verification.attempts >= 3:
                        messages.error(request, 'Too many failed attempts. Please start registration again.')
                        verification.delete()
                        return redirect('loging:CreateAccount')
                except EmailVerification.DoesNotExist:
                    pass
                
                messages.error(request, 'Invalid OTP. Please try again.')
                return render(request, "loging/otp_verification.html", {"form": form, "email": email})
        else:
            # Display form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return render(request, "loging/otp_verification.html", {"form": form, "email": email})


class CompleteRegistration(View):
    """Third step: Complete registration with user details"""
    
    def get(self, request):
        email = request.session.get('registration_email')
        if not email:
            messages.error(request, 'Please start the registration process again.')
            return redirect('loging:CreateAccount')
        
        # Check if email is verified
        try:
            verification = EmailVerification.objects.get(email=email, is_verified=True)
        except EmailVerification.DoesNotExist:
            messages.error(request, 'Please verify your email first.')
            return redirect('loging:verify_otp')
        
        form = CompleteRegistrationForm()
        return render(request, "loging/complete_registration.html", {"form": form, "email": email})
    
    def post(self, request):
        email = request.session.get('registration_email')
        if not email:
            messages.error(request, 'Please start the registration process again.')
            return redirect('loging:CreateAccount')
        
        # Check if email is verified
        try:
            verification = EmailVerification.objects.get(email=email, is_verified=True)
        except EmailVerification.DoesNotExist:
            messages.error(request, 'Please verify your email first.')
            return redirect('loging:verify_otp')
        
        form = CompleteRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=email,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    password=form.cleaned_data['password'],
                    user_type=form.cleaned_data['user_type'],
                    email_verified=True
                )
                
                # Clean up verification record
                verification.delete()
                
                # Clear session
                if 'registration_email' in request.session:
                    del request.session['registration_email']
                
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('loging:loginView')
                
            except IntegrityError:
                messages.error(request, 'An account with this username already exists. Please use a different username.')
                return render(request, "loging/complete_registration.html", {"form": form, "email": email})
        else:
            # Display form validation errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
            return render(request, "loging/complete_registration.html", {"form": form, "email": email})

class redirect_view(LoginRequiredMixin,View):
    def get(self,request):
        if hasattr(request.user, 'user_type'):
            if request.user.user_type == "Counsellor":
                date = timezone.now().date()
                if DailyLog_Counsellor.objects.filter(doctor=request.user,date=date).exists():
                     return redirect(reverse_lazy("loging:counsellor"))
                else:
                    return redirect(reverse_lazy("CounsellorIntern:daily_log_popup"))
            elif request.user.user_type == "patient":
                return redirect(reverse_lazy("userend:home"))
            elif request.user.user_type == "intern":
                return redirect(reverse_lazy("loging:intern"))
            elif request.user.user_type == "HR":
                return redirect(reverse_lazy("loging:hr_dashboard"))
        return redirect(reverse_lazy("userend:home"))

class hr(View):
    def get(self, request):
        # Check if user is authenticated and is HR
        if not request.user.is_authenticated:
            return redirect('loging:loginView')
        
        if request.user.user_type != 'HR':
            # Redirect non-HR users to appropriate dashboard
            if request.user.user_type == 'Counsellor':
                return redirect('loging:counsellor')
            elif request.user.user_type == 'patient':
                return redirect('userend:home')
            else:
                return redirect('loging:loginView')
        
        today_date = timezone.now().date()
        
        # Get statistics for HR dashboard
        # Get all counsellor doctors
        all_counsellors = CustomUser.objects.filter(user_type='Counsellor')
        total_counsellors = all_counsellors.count()
        
        # Get doctors who marked themselves present today
        present_doctors = DailyLog_Counsellor.objects.filter(date=today_date, present=True).count()
        
        # Get doctors who marked themselves absent today
        absent_doctors = DailyLog_Counsellor.objects.filter(date=today_date, present=False).count()
        
        # Calculate total absent (explicitly absent + not logged in)
        no_of_doctor_present = present_doctors
        no_of_doctor_absent = absent_doctors + (total_counsellors - present_doctors - absent_doctors)
        
        # Get appointment statistics
        no_of_appointmet_completed = Dailylog_Counserllor_patient.objects.filter(date=today_date, completed=True).count()
        no_of_appointmet_scheduled = Dailylog_Counserllor_patient.objects.filter(date=today_date, completed=False).count()
        
        # Get job application counts for active postings (expiring in next 2+ weeks)
        job_count = []
        job_id_list = JobPostedbyHR.objects.filter(
            last_date_to_apply__gte=today_date + timedelta(weeks=2)
        ).values_list('id', flat=True)
        
        for job_id in job_id_list:
            count = JobAppliedbyUser.objects.filter(job_id=job_id).count()
            name = JobPostedbyHR.objects.get(id=job_id).job_title
            job_count.append({"count": count, "name": name})
        
        return render(request, "userend/hr_dashboard.html", {
            "no_of_doctor_absent": no_of_doctor_absent,
            "no_of_doctor_present": no_of_doctor_present,
            "no_of_appointmet_completed": no_of_appointmet_completed,
            "no_of_appointmet_scheduled": no_of_appointmet_scheduled,
            "job_count": job_count
        })
        
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return render(request, "loging/logout.html")

class counsellor(View):
    def get(self, request):
        # Check if user is authenticated and is a counsellor
        if not request.user.is_authenticated:
            return redirect('loging:login')
        
        if request.user.user_type != 'Counsellor':
            # Redirect non-counsellors to appropriate dashboard
            if request.user.user_type == 'Patient':
                return redirect('userend:appointment')
            else:
                return redirect('loging:login')
        user = request.user
        current_date = timezone.now().date()
        
        # Get statistics for counsellor dashboard
        dailypatient_count_remaining = Dailylog_Counserllor_patient.objects.filter(doctor_id=request.user,date=current_date,completed=False).count()
        daily_patient_count_completed = Dailylog_Counserllor_patient.objects.filter(doctor_id=request.user,date=current_date,completed=True).count()
        this_week_total_sessions=Dailylog_Counserllor_patient.objects.filter(doctor_id=request.user,date__week=timezone.now().isocalendar()[1],completed=True).count()
        Recent_appointments=Dailylog_Counserllor_patient.objects.filter(doctor_id=request.user,date=current_date).order_by('time_slot')[:2]
        dip={
            "dailypatient_count_remaining": dailypatient_count_remaining,
            "daily_patient_count_completed": daily_patient_count_completed,
            "this_week_total_sessions": this_week_total_sessions,
            "Recent_appointments": Recent_appointments
        }
        return render(request, "userend/dashboard.html",dip)

class intern(View):
    def get(self, request):
        return render(request, "userend/genz_dashboard.html")

# class how_it_works(View):
#     def get(self, request):
#         return render(request, "userend/how_it_works.html")

# class list_psychologists(View):
#     def get(self, request):
#         return render(request, "userend/list_psychologists.html")
