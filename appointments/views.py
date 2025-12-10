"Appointment booking view"
import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
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

def index(request, service_id=None, service_ids=None, hairdresser_id=None, date_string=None):
    "View for selecting service, hairdresser, date and time"
    
    # Auto-create admin user if it doesn't exist
    from django.contrib.auth.models import User
    import os
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    password = os.environ.get('ADMIN_PASSWORD', 'LuxHair2025!')
    if not User.objects.filter(username=username).exists() and password:
        try:
            User.objects.create_superuser(
                username=username,
                email=os.environ.get('ADMIN_EMAIL', 'admin@luxehairstudio.com'),
                password=password
            )
        except Exception:
            pass  # Ignore errors, admin creation is optional
    
    services = Service.objects.all()
    context = {"services_all": services}

    # Try to get announcements from DynamoDB, but don't fail if not available
    try:
        if dynamodb is not None:
            print("DynamoDB client exists, attempting to fetch announcements...")
            announcements = dynamodb.scan(TableName="DEV_Announcement")
            announcement_list = [a['Contents']['S'] for a in announcements['Items']]
            print(f"Successfully fetched {len(announcement_list)} announcements: {announcement_list}")
            context["announcements"] = announcement_list
        else:
            print("DynamoDB client is None - AWS credentials not configured")
            context["announcements"] = ["DEBUG: DynamoDB client not available"]
    except Exception as e:
        print(f"Error fetching announcements: {str(e)}")
        context["announcements"] = [f"DEBUG: Error fetching announcements - {str(e)}"]

    # Handle both single service and multiple services
    selected_services = []
    if service_id:
        selected_services = [service_id]
        context["selected_service_id"] = service_id
    elif service_ids:
        try:
            selected_services = [int(sid) for sid in service_ids.split(',') if sid.strip()]
            context["selected_service_ids"] = selected_services
        except ValueError:
            selected_services = []

    if selected_services:
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
                
                # Calculate total duration for multiple services
                total_duration = sum(
                    Service.objects.get(service_id=sid).duration 
                    for sid in selected_services
                )
                
                start_times = build_start_times(
                    day_start, total_duration, blocked_times
                )

                context["start_times_all"] = start_times
                context["start_times_available_count"] = len(
                    [t for t in start_times if not t["is_blocked"]]
                )
                
                # Add selected services info for display
                context["selected_services"] = Service.objects.filter(service_id__in=selected_services)
                context["total_price"] = sum(s.price for s in context["selected_services"])
                context["total_duration"] = total_duration

    # Clear booking success data after displaying it once
    if 'booking_success' in request.session:
        del request.session['booking_success']
    
    return render(request, "appointments/index.html", context)

def create(request):
    "View for creating an appointment"
    if request.method == "POST":
        service_ids_str = request.POST.get("services")  # Changed from "service" to "services"
        hairdresser_id = request.POST.get("hairdresser")
        date_string = request.POST.get("date")
        appointment_time = request.POST.get("appointment_time")
        customer_contact = request.POST.get("customer_contact")

        # Parse service IDs
        try:
            service_ids = [int(sid) for sid in service_ids_str.split(',') if sid.strip()]
        except (ValueError, AttributeError):
            # Fallback to single service for backward compatibility
            service_id = request.POST.get("service")
            service_ids = [int(service_id)] if service_id else []

        if not service_ids:
            messages.error(request, "Please select at least one service.")
            return HttpResponseRedirect(reverse("index"))

        services = Service.objects.filter(service_id__in=service_ids)
        hairdresser = Hairdresser.objects.get(hairdresser_id=hairdresser_id)
        
        start_datetime = timezone.make_aware(
            datetime.datetime.strptime(
                date_string + " " + appointment_time, "%Y%m%d %I:%M %p"
            )
        )

        # Create appointments for each service (sequential booking)
        current_start = start_datetime
        appointments = []
        cancel_urls = []

        for service in services:
            end_datetime = current_start + datetime.timedelta(minutes=service.duration)

            # Generate cancellation token
            import secrets
            cancellation_token = secrets.token_urlsafe(32)

            appointment = Appointment.objects.create(
                service=service,
                hairdresser=hairdresser,
                start_datetime=current_start,
                end_datetime=end_datetime,
                customer_contact=customer_contact,
                cancellation_token=cancellation_token,
            )
            
            appointments.append(appointment)
            
            # Build cancellation URL
            cancel_url = request.build_absolute_uri(
                reverse("cancel", args=[cancellation_token])
            )
            cancel_urls.append(f"{service.service_name}: {cancel_url}")
            
            # Next service starts when this one ends
            current_start = end_datetime

        # Create summary message
        service_names = [s.service_name for s in services]
        total_price = sum(s.price for s in services)
        
        # Create structured cancellation data for template
        cancellation_data = []
        for cancel_url in cancel_urls:
            service_name, url = cancel_url.split(': ', 1)
            token = url.split('/')[-2]  # Extract token from URL
            cancellation_data.append({
                'service_name': service_name,
                'url': url,
                'token': token
            })
        
        # Store comprehensive appointment data in session for template access
        request.session['booking_success'] = {
            'services': service_names,
            'total_price': float(total_price),
            'hairdresser_name': f"{hairdresser.first_name} {hairdresser.last_name}",
            'appointment_date': start_datetime.strftime("%A, %B %d, %Y"),
            'appointment_time': start_datetime.strftime("%I:%M %p"),
            'customer_contact': customer_contact,
            'cancellation_data': cancellation_data
        }
        
        # Create detailed success message
        hairdresser_name = f"{hairdresser.first_name} {hairdresser.last_name}"
        appointment_date = start_datetime.strftime("%A, %B %d, %Y")
        appointment_time = start_datetime.strftime("%I:%M %p")
        
        messages.success(
            request, 
            f"✅ Your appointments have been created successfully! "
            f"Services: {', '.join(service_names)} | "
            f"Stylist: {hairdresser_name} | "
            f"Date: {appointment_date} | "
            f"Time: {appointment_time} | "
            f"Total: ${total_price}"
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

def setup_admin(request):
    """Create admin user - for initial setup only"""
    from django.contrib.auth.models import User
    import os
    
    username = os.environ.get('ADMIN_USERNAME', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@luxehairstudio.com')
    password = os.environ.get('ADMIN_PASSWORD', 'LuxHair2025!')
    
    if User.objects.filter(username=username).exists():
        return HttpResponse(f'Admin user "{username}" already exists!')
    
    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    
    return HttpResponse(f'Admin user "{username}" created successfully! You can now login at /admin/')