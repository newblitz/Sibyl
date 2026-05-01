from django import forms
from .models import DailyLog_Counsellor, DailyNotification_Counsellor, Dailylog_Counserllor_patient

class DailyLog_CounsellorFormpopup(forms.ModelForm):
    class Meta:
        model = DailyLog_Counsellor
        fields = ['present', 'working_day']
        widgets = {
            'present': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'working_day': forms.Select(attrs={'class': 'form-control'}),
        }

class DailyNotification_CounsellorForm(forms.ModelForm):
    class Meta:
        model = DailyNotification_Counsellor
        fields = ['time_slot']
        widgets = {
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            
        }
class DailyCousellorForm(forms.ModelForm):
    time_slot_choices = [("09:00","09:00"),("10:00","10:00"),("11:00","11:00"),("14:00","14:00"),("15:00","15:00"),("16:00","16:00")]
    name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Dailylog_Counserllor_patient
        fields = ['time_slot', 'meeting_link','date','completed']
        widgets = {
            'time_slot': forms.Select(attrs={'class': 'form-control'}),
            'meeting_link': forms.URLInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }