from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
import os


class Command(BaseCommand):
    help = 'Create admin user (demo mode creates public access)'

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
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS('Successfully created demo admin user - public access enabled')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS('Demo admin user already exists - public access enabled')
                )
        else:
            # Production mode - require environment variables
            username = os.environ.get('ADMIN_USERNAME')
            email = os.environ.get('ADMIN_EMAIL')
            password = os.environ.get('ADMIN_PASSWORD')
            
            if not all([username, email, password]):
                self.stdout.write(
                    self.style.ERROR('Please set ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD environment variables')
                )
                return
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            
            if not created:
                user.email = email
                user.is_staff = True
                user.is_superuser = True
            
            user.set_password(password)
            user.save()
            
            action = 'Created' if created else 'Updated'
            self.stdout.write(
                self.style.SUCCESS(f'{action} admin user: {username}')
            )