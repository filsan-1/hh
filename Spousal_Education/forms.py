from django import forms
from .models import ArticleComment


class ArticleCommentForm(forms.ModelForm):
    """Form for adding comments to articles"""
    
    class Meta:
        model = ArticleComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your thoughts or questions...',
                'style': 'resize: vertical;'
            })
        }
        labels = {
            'content': 'Your Comment'
        }
