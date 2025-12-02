import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hairdresser_django.settings')
django.setup()

from appointments.models import Service

# Update existing services
services_data = [
    {'service_id': 1, 'service_name': 'Manicure', 'description': 'Professional nail care and polish', 'duration': 45, 'price': 35},
    {'service_id': 2, 'service_name': 'Pedicure', 'description': 'Foot care and nail treatment', 'duration': 60, 'price': 50},
    {'service_id': 3, 'service_name': 'Nail Enhancements', 'description': 'Acrylic or gel nail extensions', 'duration': 90, 'price': 65},
]

for data in services_data:
    service = Service.objects.get(service_id=data['service_id'])
    service.service_name = data['service_name']
    service.description = data['description']
    service.duration = data['duration']
    service.price = data['price']
    service.save()
    print(f"Updated: {service.service_name}")

print("All services updated!")
