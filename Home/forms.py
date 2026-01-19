from django import forms
from .models import Period, Symptom
from datetime import date

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your Message'}), max_length=2000)

class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['start_date', 'end_date', 'cycle_length', 'flow', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'required': True
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'Leave empty if ongoing'
            }),
            'cycle_length': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '20', 
                'max': '45', 
                'value': '28',
                'placeholder': 'Average cycle length (20-45 days)'
            }),
            'flow': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Any additional notes about this period (optional)'
            }),
        }
        labels = {
            'start_date': '📅 Start Date',
            'end_date': '📅 End Date (optional)',
            'cycle_length': '🔄 Cycle Length',
            'flow': '💧 Flow Intensity',
            'notes': '📝 Notes',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and start_date > date.today():
            raise forms.ValidationError("Start date cannot be in the future.")
        
        if end_date and start_date and end_date < start_date:
            raise forms.ValidationError("End date cannot be before start date.")
        
        if end_date and end_date > date.today():
            raise forms.ValidationError("End date cannot be in the future.")
        
        return cleaned_data

class SymptomForm(forms.ModelForm):
    class Meta:
        model = Symptom
        fields = ['date', 'symptom_type', 'severity', 'mood', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control'
            }),
            'symptom_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'severity': forms.NumberInput(attrs={
                'class': 'form-control', 
                'min': '1', 
                'max': '10', 
                'placeholder': 'Rate from 1 (mild) to 10 (severe)'
            }),
            'mood': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 3, 
                'placeholder': 'Additional details about your symptom (optional)'
            }),
        }
        labels = {
            'date': '📅 Date',
            'symptom_type': '🩺 Symptom Type',
            'severity': '📊 Severity Level',
            'mood': '😊 Mood',
            'notes': '📝 Notes',
        }
    
    def clean_date(self):
        symptom_date = self.cleaned_data.get('date')
        if symptom_date and symptom_date > date.today():
            raise forms.ValidationError("Symptom date cannot be in the future.")
        return symptom_date
