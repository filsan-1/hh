from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)

class PeriodForm(forms.Form):
    start_date = forms.DateField()
    end_date = forms.DateField()

class SymptomForm(forms.Form):
    symptom_name = forms.CharField(max_length=100)
    severity = forms.IntegerField()
