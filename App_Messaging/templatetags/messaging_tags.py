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

@register.filter
def has_unread_messages(conversation, user):
    """Check if conversation has unread messages from other users"""
    try:
        return conversation.messages.filter(is_read=False).exclude(sender=user).exists()
    except:
        return False
