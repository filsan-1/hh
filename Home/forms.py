from django import forms
from .models import Period, Symptom

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)

class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['start_date', 'end_date', 'cycle_length']

class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['date', 'symptom', 'severity', 'notes']
