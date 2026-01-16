from django import forms
from .models import HormonalTwin, TwinConnection

class HormonalTwinProfileForm(forms.ModelForm):
    class Meta:
        model = HormonalTwin
        fields = ['primary_issue', 'secondary_issues', 'bio', 'profile_picture']
        widgets = {
            'primary_issue': forms.Select(attrs={'class': 'form-control'}),
            'secondary_issues': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Heavy Bleeding, Hormonal Acne'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your story...'
            }),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class TwinConnectionForm(forms.ModelForm):
    class Meta:
        model = TwinConnection
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Say hello! (optional)'
            }),
        }
