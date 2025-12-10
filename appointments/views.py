"Appointment booking view"
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
import boto3
from botocore.exceptions import NoRegionError

from .models import Service, Hairdresser, Appointment

# Try to create DynamoDB client, but don't fail if AWS not configured
try:
    dynamodb = boto3.client("dynamodb", region_name="us-east-1")
except Exception:
    dynamodb = None


def intervals_overlap(startime_1, end1, startime_2, end2):
    "Check if one interval starts after the other one ends"
    return not (end1 <= startime_2 or end2 <= startime_1)

def build_start_times(day_start, service_duration, blocked_times):
    "Build a list of start times for a given day"
    start_times = []
    for mins in range(0, 540, 30):
        time_1 = day_start + datetime.timedelta(minutes=mins)
        time_2 = time_1 + datetime.timedelta(minutes=service_duration)
        is_blocked = False

        # Don't allow appointments in the past.
        if time_1 < timezone.now():
            is_blocked = True
        else:
            # Test if the start time will overlap with any of the blocked times.
            for time in blocked_times:
                if intervals_overlap(time[0], time[1], time_1, time_2):
                    is_blocked = True

        start_times.append(
            {"time_formatted": time_1.strftime("%I:%M %p"), "is_blocked": is_blocked}
        )
    return start_times

def index(request, service_id=None, hairdresser_id=None, date_string=None):
    "View for selecting service, hairdresser, date and time"
    services = Service.objects.all()
    context = {"services_all": services}

    # Try to get announcements from DynamoDB, but don't fail if not available
    try:
        announcements = dynamodb.scan(TableName="DEV_Announcement")
        context["announcements"] = [a['Contents']['S'] for a in announcements['Items']]
    except Exception:
        context["announcements"] = []

    if service_id:
        context["selected_service_id"] = service_id
        context["hairdressers_all"] = Hairdresser.objects.all()

        if hairdresser_id:
            context["selected_hairdresser_id"] = hairdresser_id
            today = timezone.now().date()
            upcoming_dates = [(today + datetime.timedelta(days=d)) for d in range(7)]
            context["dates_all"] = [
                (d.strftime("%a %d %B"), d.strftime("%Y%m%d")) for d in upcoming_dates
            ]

            if date_string:
                # Find the "unavailable times".
                parsed_datetime = timezone.make_aware(
                    datetime.datetime.strptime(date_string, "%Y%m%d")
                )

                # We could write the filter to restrict to day.
                appointments = Appointment.objects.filter(
                    hairdresser__pk=hairdresser_id
                )
                blocked_times = [
                    (appt.start_datetime, appt.end_datetime)
                    for appt in appointments
                    if appt.start_datetime.date() == parsed_datetime.date()
                ]

                context["selected_date"] = date_string

                day_start = parsed_datetime.replace(
                    hour=9, minute=0, second=0, microsecond=0
                )
                service_duration = Service.objects.get(service_id=service_id).duration
                start_times = build_start_times(
                    day_start, service_duration, blocked_times
                )

                context["start_times_all"] = start_times
                context["start_times_available_count"] = len(
                    [t for t in start_times if not t["is_blocked"]]
                )

    return render(request, "appointments/index.html", context)

def create(request):
    "View for creating an appointment"
    if request.method == "POST":
        service_id = request.POST.get("service")
        hairdresser_id = request.POST.get("hairdresser")
        date_string = request.POST.get("date")
        appointment_time = request.POST.get("appointment_time")
        customer_contact = request.POST.get("customer_contact")

        service = Service.objects.get(service_id=service_id)
        hairdresser = Hairdresser.objects.get(hairdresser_id=hairdresser_id)
        start_datetime = timezone.make_aware(
            datetime.datetime.strptime(
                date_string + " " + appointment_time, "%Y%m%d %I:%M %p"
            )
        )
        end_datetime = start_datetime + datetime.timedelta(minutes=service.duration)

        # Generate cancellation token
        import secrets
        cancellation_token = secrets.token_urlsafe(32)

        appointment = Appointment.objects.create(
            service=service,
            hairdresser=hairdresser,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            customer_contact=customer_contact,
            cancellation_token=cancellation_token,
        )
        
        # Build cancellation URL
        cancel_url = request.build_absolute_uri(
            reverse("cancel", args=[cancellation_token])
        )
        
        messages.info(
            request, 
            f"Your appointment has been created. To cancel, visit: {cancel_url}"
        )

    return HttpResponseRedirect(reverse("index"))


def cancel(request, token):
    "View for cancelling an appointment"
    try:
        appointment = Appointment.objects.get(cancellation_token=token, is_cancelled=False)
        
        if request.method == "POST":
            appointment.is_cancelled = True
            appointment.save()
            messages.success(request, "Your appointment has been cancelled.")
            return HttpResponseRedirect(reverse("index"))
        
        return render(request, "appointments/cancel.html", {"appointment": appointment})
    
    except Appointment.DoesNotExist:
        messages.error(request, "Invalid cancellation link or appointment already cancelled.")
        return HttpResponseRedirect(reverse("index"))
