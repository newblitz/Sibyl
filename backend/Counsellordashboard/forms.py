from CounsellorIntern.models import DailyNotification_Counsellor
from django import forms

class DailyNotification_CounsellorForm(forms.ModelForm):
    class Meta:
        model = DailyNotification_Counsellor
        fields = ['approved']
        widgets = {
            'approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }