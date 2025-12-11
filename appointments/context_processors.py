"""Context processor to make business config available in templates"""
from django.conf import settings

def business_config(request):
    """Add business configuration to template context"""
    return {
        'BUSINESS_TYPE': settings.BUSINESS_TYPE,
        'BUSINESS_NAME': settings.BUSINESS_NAME,
        'PROVIDER_TITLE': settings.PROVIDER_TITLE,
        'PROVIDER_TITLE_PLURAL': settings.PROVIDER_TITLE_PLURAL,
        'PRIMARY_COLOR': settings.PRIMARY_COLOR,
        'SECONDARY_COLOR': settings.SECONDARY_COLOR,
        'ACCENT_COLOR': settings.ACCENT_COLOR,
        'BACKGROUND_COLOR': settings.BACKGROUND_COLOR,
        'DEMO_MODE': getattr(settings, 'DEMO_MODE', False),
        'settings': settings,  # Make settings available in templates
    }
