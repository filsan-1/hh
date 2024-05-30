from django import forms
from .models import PeriodLog, SymptomLog

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.CharField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)

class PeriodLogForm(forms.ModelForm):
    class Meta:
        model = PeriodLog
        fields = ['start_date', 'end_date', 'cycle_length']

class SymptomLogForm(forms.ModelForm):
    class Meta:
        model = SymptomLog
        fields = ['date', 'symptom', 'severity', 'notes']
