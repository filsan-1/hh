from django.test import TestCase
from django.contrib.auth.models import User
from .models import Conversation, Message


class ConversationModelTest(TestCase):
    """Test Conversation model"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
    
    def test_create_conversation(self):
        """Test creating a conversation"""
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        
        self.assertEqual(conversation.participants.count(), 2)
        self.assertIn(self.user1, conversation.participants.all())
        self.assertIn(self.user2, conversation.participants.all())
    
    def test_get_other_user(self):
        """Test getting the other user in a conversation"""
        conversation = Conversation.objects.create()
        conversation.participants.add(self.user1, self.user2)
        
        other_user = conversation.get_other_user(self.user1)
        self.assertEqual(other_user, self.user2)
        
        other_user = conversation.get_other_user(self.user2)
        self.assertEqual(other_user, self.user1)


class MessageModelTest(TestCase):
    """Test Message model"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        
        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user1, self.user2)
    
    def test_create_message(self):
        """Test creating a message"""
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Hello!'
        )
        
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.content, 'Hello!')
        self.assertFalse(message.is_read)
    
    def test_mark_message_as_read(self):
        """Test marking a message as read"""
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content='Hello!'
        )
        
        self.assertFalse(message.is_read)
        message.mark_as_read()
        
        message.refresh_from_db()
        self.assertTrue(message.is_read)
