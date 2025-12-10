from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create admin user'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@luxehairstudio.com',
                password='LuxHair2025!'
            )
            self.stdout.write(
                self.style.SUCCESS('Successfully created admin user')
            )
        else:
            # Update password if user exists
            admin_user = User.objects.get(username='admin')
            admin_user.set_password('LuxHair2025!')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS('Updated admin user password')
            )