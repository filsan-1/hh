from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from App_Messaging.models import Conversation, Message


class Command(BaseCommand):
    help = 'Create test data for messaging system'

    def handle(self, *args, **kwargs):
        # Create test users
        user1, created1 = User.objects.get_or_create(
            username='alice',
            defaults={
                'email': 'alice@example.com',
                'first_name': 'Alice',
                'last_name': 'Smith'
            }
        )
        if created1:
            user1.set_password('password123')
            user1.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: alice'))

        user2, created2 = User.objects.get_or_create(
            username='bob',
            defaults={
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Johnson'
            }
        )
        if created2:
            user2.set_password('password123')
            user2.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: bob'))

        # Create a conversation
        conversation, created = Conversation.objects.get_or_create(
            id=1
        )
        if created:
            conversation.participants.add(user1, user2)
            self.stdout.write(self.style.SUCCESS(f'Created conversation between alice and bob'))

            # Create sample messages
            Message.objects.create(
                conversation=conversation,
                sender=user1,
                content="Hi Bob! How are you doing?"
            )
            Message.objects.create(
                conversation=conversation,
                sender=user2,
                content="Hi Alice! I'm doing great, thanks for asking. How about you?"
            )
            Message.objects.create(
                conversation=conversation,
                sender=user1,
                content="I'm good too! Just wanted to check in about our plans for this weekend."
            )
            self.stdout.write(self.style.SUCCESS(f'Created sample messages'))
        else:
            self.stdout.write(self.style.WARNING('Conversation already exists'))

        self.stdout.write(self.style.SUCCESS('Test data setup complete!'))
        self.stdout.write(self.style.SUCCESS('You can login with:'))
        self.stdout.write(self.style.SUCCESS('  Username: alice / Password: password123'))
        self.stdout.write(self.style.SUCCESS('  Username: bob / Password: password123'))
