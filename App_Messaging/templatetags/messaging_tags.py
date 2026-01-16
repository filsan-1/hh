from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def get_other_user(conversation, user):
    """Get the other participant in a conversation"""
    try:
        other_user = conversation.participants.exclude(id=user.id).first()
        return other_user.get_full_name() or other_user.username if other_user else "Unknown User"
    except:
        return "Unknown User"

@register.filter
def get_other_user_object(conversation, user):
    """Get the other participant object in a conversation"""
    try:
        return conversation.participants.exclude(id=user.id).first()
    except:
        return None
