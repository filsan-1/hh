from django import forms
from .models import Period, Symptom

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}), max_length=2000)

class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['start_date', 'end_date', 'cycle_length']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cycle_length': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cycle length in days'}),
        }

class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['date', 'symptom', 'severity', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'symptom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Headache, Cramps, Bloating'}),
            'severity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10', 'placeholder': 'Rate 1-10'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes (optional)'}),
        }
