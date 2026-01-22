"""
Management command to check password hashing algorithms
and provide information about upgrading password security
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import identify_hasher


class Command(BaseCommand):
    help = 'Check which password hashing algorithm is being used for users'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Checking password hashing algorithms...\n'))
        
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write(self.style.WARNING('No users found in the database.'))
            return
        
        hasher_stats = {}
        total_users = users.count()
        
        for user in users:
            try:
                hasher = identify_hasher(user.password)
                hasher_name = hasher.algorithm
                hasher_stats[hasher_name] = hasher_stats.get(hasher_name, 0) + 1
            except ValueError:
                hasher_stats['invalid'] = hasher_stats.get('invalid', 0) + 1
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal Users: {total_users}\n'))
        self.stdout.write(self.style.SUCCESS('Password Hashing Statistics:'))
        self.stdout.write('-' * 50)
        
        for hasher_name, count in hasher_stats.items():
            percentage = (count / total_users) * 100
            if hasher_name == 'argon2':
                style = self.style.SUCCESS
                status = '✓ SECURE'
            elif hasher_name in ['pbkdf2_sha256', 'bcrypt_sha256', 'bcrypt']:
                style = self.style.WARNING
                status = '⚠ ACCEPTABLE'
            else:
                style = self.style.ERROR
                status = '✗ INSECURE'
            
            self.stdout.write(
                style(f'{hasher_name:20} : {count:4} users ({percentage:5.1f}%) {status}')
            )
        
        # Provide recommendations
        self.stdout.write('\n' + '=' * 50)
        
        if 'argon2' in hasher_stats and hasher_stats['argon2'] == total_users:
            self.stdout.write(self.style.SUCCESS(
                '\n✓ All passwords are using Argon2 hashing. Security is optimal!'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                '\n⚠ Some passwords are not using Argon2 hashing.'
            ))
            self.stdout.write('\nRecommendations:')
            self.stdout.write('1. Passwords will automatically upgrade to Argon2 when users log in')
            self.stdout.write('2. For immediate upgrade, ask users to change their passwords')
            self.stdout.write('3. Or use: python manage.py changepassword <username>')
            
        self.stdout.write('')
