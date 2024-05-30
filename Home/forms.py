from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)

class PeriodForm(forms.Form):
    # Define the fields for the PeriodForm
    pass

class SymptomForm(forms.Form):
    # Define the fields for the SymptomForm
    pass


    
