from django import forms
from .models import SupportCircle, CirclePost, CircleComment

class SupportCircleForm(forms.ModelForm):
    class Meta:
        model = SupportCircle
        fields = ['name', 'description', 'focus_area', 'is_private']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Circle Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What is this circle about?'
            }),
            'focus_area': forms.Select(attrs={'class': 'form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CirclePostForm(forms.ModelForm):
    class Meta:
        model = CirclePost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post Title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your thoughts...'
            }),
        }

class CircleCommentForm(forms.ModelForm):
    class Meta:
        model = CircleComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Add a comment...'
            }),
        }
