"""
Custom authentication backend for demo mode
"""
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.conf import settings


class DemoAdminBackend(BaseBackend):
    """
    Authentication backend that allows public access to admin in demo mode
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Always authenticate as demo admin user for demo purposes
        """
        # Only work in demo mode
        if not getattr(settings, 'DEMO_MODE', False):
            return None
            
        # Create or get demo admin user
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
        
        # Ensure user has admin privileges
        if not demo_user.is_staff or not demo_user.is_superuser:
            demo_user.is_staff = True
            demo_user.is_superuser = True
            demo_user.save()
            
        return demo_user
    
    def get_user(self, user_id):
        """
        Get user by ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class PublicAdminMiddleware:
    """
    Middleware to automatically log in users as demo admin for admin pages
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Auto-login for admin pages in demo mode
        if (getattr(settings, 'DEMO_MODE', False) and 
            request.path.startswith('/admin/') and 
            not request.user.is_authenticated):
            
            from django.contrib.auth import login
            
            # Get or create demo admin user
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
            
            # Ensure user has admin privileges
            if not demo_user.is_staff or not demo_user.is_superuser:
                demo_user.is_staff = True
                demo_user.is_superuser = True
                demo_user.save()
            
            # Log in the user
            login(request, demo_user, backend='appointments.auth_backends.DemoAdminBackend')
        
        response = self.get_response(request)
        return response