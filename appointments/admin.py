from django.contrib import admin
from .models import Service, Hairdresser, Appointment


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'price', 'duration')
    search_fields = ('service_name',)
    list_filter = ('price',)


@admin.register(Hairdresser)
class HairdresserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'hairdresser', 'service', 'start_datetime', 'is_cancelled')
    list_filter = ('is_cancelled', 'hairdresser', 'service', 'start_datetime')
    search_fields = ('customer_contact',)
    readonly_fields = ('cancellation_token',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('hairdresser', 'service')
