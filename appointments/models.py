"Models for the appointment booking app"
from django.db import models

class Service(models.Model):
    "Services offered (e.g., haircut, manicure, pedicure)"
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()

    def __str__(self):
        return self.service_name

class Hairdresser(models.Model):
    "Service provider (hairdresser, nail technician, etc.)"
    hairdresser_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Service Provider"
        verbose_name_plural = "Service Providers"

class Appointment(models.Model):
    "Customer appointments"
    appointment_id = models.AutoField(primary_key=True)
    hairdresser = models.ForeignKey(Hairdresser, on_delete=models.CASCADE, verbose_name="Provider")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    customer_contact = models.TextField()
    is_cancelled = models.BooleanField(default=False)
    cancellation_token = models.CharField(max_length=64, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.service} - {self.start_datetime}"
