from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = 'Create a superuser account'

    def handle(self, *args, **options):
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@luxehairstudio.com')
        password = os.environ.get('ADMIN_PASSWORD', 'LuxHair2025!')
        
        self.stdout.write(f'Attempting to create superuser: {username}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Password set: {"Yes" if password else "No"}')
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists')
            )
            # Update password in case it changed
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Updated password for superuser "{username}"')
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