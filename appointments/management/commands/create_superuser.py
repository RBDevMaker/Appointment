from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Create a superuser account'

    def handle(self, *args, **options):
        if getattr(settings, 'DEMO_MODE', False):
            # In demo mode, create demo admin user
            demo_user, created = User.objects.get_or_create(
                username='demo_admin',
                defaults={
                    'email': 'demo@luxehairstudio.com',
                    'is_staff': True,
                    'is_superuser': True,
                    'first_name': 'Demo',
                    'last_name': 'Admin'
                }
            )
            
            action = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(f'{action} demo superuser - public admin access enabled')
            )
            return
        
        # Production mode - require environment variables
        username = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')
        
        if not all([username, email, password]):
            self.stdout.write(
                self.style.ERROR('Please set ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD environment variables')
            )
            return
        
        self.stdout.write(f'Attempting to create superuser: {username}')
        self.stdout.write(f'Email: {email}')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists')
            )
            # Update password in case it changed
            user = User.objects.get(username=username)
            user.set_password(password)
            user.email = email
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated superuser "{username}"')
            )
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully')
            )