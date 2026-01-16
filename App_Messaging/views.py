from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.contrib import messages as django_messages
from .models import Conversation, Message
from .forms import MessageForm, StartConversationForm


@login_required
def conversation_list(request):
    """Display list of all conversations for the current user"""
    user = request.user
    conversations = user.conversations.all()
    
    context = {
        'conversations': conversations,
        'page_title': 'Messages',
    }
    return render(request, 'App_Messaging/conversation_list.html', context)


@login_required
def conversation_detail(request, conversation_id):
    """Display messages in a specific conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check if user is part of this conversation
    if request.user not in conversation.participants.all():
        django_messages.error(request, 'You do not have access to this conversation.')
        return redirect('App_Messaging:conversation_list')
    
    # Mark messages as read
    unread_messages = conversation.messages.filter(~Q(sender=request.user), is_read=False)
    for message in unread_messages:
        message.mark_as_read()
    
    form = MessageForm()
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            return redirect('App_Messaging:conversation_detail', conversation_id=conversation.id)
    
    messages = conversation.messages.all()
    other_user = conversation.get_other_user(request.user)
    
    context = {
        'conversation': conversation,
        'messages': messages,
        'form': form,
        'other_user': other_user,
        'page_title': f'Chat with {other_user.get_full_name() or other_user.username}',
    }
    return render(request, 'App_Messaging/conversation_detail.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def start_conversation(request):
    """Start a new conversation with a user"""
    form = StartConversationForm(current_user=request.user)
    
    if request.method == 'POST':
        form = StartConversationForm(request.POST, current_user=request.user)
        if form.is_valid():
            recipient = form.cleaned_data['recipient']
            
            # Check if conversation already exists
            existing_conversation = Conversation.objects.filter(
                participants=request.user
            ).filter(
                participants=recipient
            ).first()
            
            if existing_conversation:
                return redirect('App_Messaging:conversation_detail', conversation_id=existing_conversation.id)
            
            # Create new conversation
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, recipient)
            
            django_messages.success(request, f'Conversation started with {recipient.username}!')
            return redirect('App_Messaging:conversation_detail', conversation_id=conversation.id)
    
    context = {
        'form': form,
        'page_title': 'Start New Conversation',
    }
    return render(request, 'App_Messaging/start_conversation.html', context)


@login_required
def delete_conversation(request, conversation_id):
    """Delete a conversation"""
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check if user is part of this conversation
    if request.user not in conversation.participants.all():
        django_messages.error(request, 'You do not have access to this conversation.')
        return redirect('App_Messaging:conversation_list')
    
    if request.method == 'POST':
        conversation.delete()
        django_messages.success(request, 'Conversation deleted successfully.')
        return redirect('App_Messaging:conversation_list')
    
    context = {
        'conversation': conversation,
        'page_title': 'Delete Conversation',
    }
    return render(request, 'App_Messaging/delete_conversation.html', context)


@login_required
def unread_count(request):
    """Get count of unread messages for the current user"""
    count = Message.objects.filter(
        conversation__participants=request.user,
        is_read=False
    ).exclude(sender=request.user).count()
    return {'unread_count': count}
