from django.db import migrations
from django.contrib.auth.models import User


def reset_admin_password(apps, schema_editor):
    """Reset admin user password to ensure it's correct"""
    try:
        admin_user = User.objects.get(username='admin')
        admin_user.set_password('LuxHair2025!')
        admin_user.save()
        print("Admin password reset successfully")
    except User.DoesNotExist:
        # Create admin user if it doesn't exist
        User.objects.create_superuser(
            username='admin',
            email='admin@luxehairstudio.com',
            password='LuxHair2025!'
        )
        print("Admin user created successfully")


def reverse_reset(apps, schema_editor):
    """No reverse operation needed"""
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('appointments', '0011_create_admin_user'),
    ]

    operations = [
        migrations.RunPython(reset_admin_password, reverse_reset),
    ]