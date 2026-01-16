from django import forms
from django.contrib.auth.models import User
from .models import Message, Conversation


class MessageForm(forms.ModelForm):
    """Form for creating and sending messages"""
    
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your message here...',
                'style': 'resize: vertical;'
            })
        }
        labels = {
            'content': ''
        }


class StartConversationForm(forms.Form):
    """Form for starting a new conversation"""
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'recipient-select'
        }),
        label='Select a user to message',
        empty_label='-- Choose a user --'
    )
    
    def __init__(self, *args, current_user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if current_user:
            # Exclude current user from the list
            self.fields['recipient'].queryset = User.objects.exclude(
                id=current_user.id
            ).order_by('username')
