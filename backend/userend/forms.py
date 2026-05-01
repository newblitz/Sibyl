from django import forms
from .models import Appointment
from CounsellorIntern.models import Psychologist
from django.core.validators import RegexValidator,EmailValidator,MaxValueValidator
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from CounsellorIntern.models import DailyLog_Counsellor
from datetime import datetime
class AppointmentForm(forms.ModelForm):
    today_time=datetime.now().time().hour
    time_slot_av = [("09:00","09:00"),("10:00","10:00"),("11:00","11:00"),("14:00","14:00"),("15:00","15:00"),("16:00","16:00")]
    
   
    time_slot=forms.ChoiceField(choices=time_slot_av)
    class Meta:
        model = Appointment
        today_time=datetime.now().time()
        time_slot_choices = [9,10,11,14,15,16]
        # available_doctors = DailyLog_Counsellor.objects.filter(present=True,time_slot__gt=today_time).values_list('doctor', flat=True)
        # list_of_available_slots=filter(lambda x:True if x>int(datetime.now().time().hour) else False,time_slot_choices)
        # available_doctors = DailyLog_Counsellor.objects.filter(present=True).values_list('doctor', flat=True)
        exclude=['user','IsPending','Assigned_doctor','date']  # Exclude date field as it will be auto-populated
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select your preferred date', 'value': '', 'autocomplete': 'off'}),
            'time_slot': forms.RadioSelect(attrs={'class': 'time-slot-radio'}),
            'selected_doctor': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose your preferred doctor'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            # 'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Select your preferred date'}),

            # 'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your 10-digit phone number'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select your gender'}),
            'duration': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select session duration'}),
            'session_type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Select session type'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the choices for the doctor field
        try:
            self.fields['selected_doctor'].queryset = Psychologist.objects.all()
            self.fields['selected_doctor'].empty_label = "Select a Doctor"
        except Exception as e:
            # Temporarily handle database issues
            self.fields['selected_doctor'].queryset = Psychologist.objects.none()
            self.fields['selected_doctor'].empty_label = "No doctors available"
        
        # Set date constraints for 3-day limit
        today = date.today()
        max_date = today + timedelta(days=3)
        
        # Set min and max attributes for the date input and ensure no default value
        self.fields['appointment_date'].widget.attrs.update({
            'min': today.strftime('%Y-%m-%d'),
            'max': max_date.strftime('%Y-%m-%d'),
            'value': '',  # Explicitly set empty value
            'autocomplete': 'off'  # Prevent browser autofill
        })
    
    def clean_appointment_date(self):
        # Let the view handle date validation to provide better error messages
        appointment_date = self.cleaned_data.get('appointment_date')
        return appointment_date
    