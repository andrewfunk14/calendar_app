from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware, is_naive
from datetime import datetime
from .models import Event
from django.shortcuts import render

@login_required
def calendar_view(request, year=None, month=None):
    # If year and month are not provided, default to the current year and month
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month

    # Filter events based on the selected year and month
    events = Event.objects.filter(start_time__year=year, start_time__month=month)

    # Create a range for the hours
    hours_range = range(1, 13)

    # Render the calendar template and pass the filtered events and date context
    return render(request, 'events/calendar.html', {
        'year': year,
        'month': month,
        'events': events,
        'hours_range': hours_range  # Pass the range to the template
    })

# Fetch Events as JSON (for FullCalendar)
def events_json(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    if start and end:
        try:
            # Convert string dates to datetime objects
            start_date = datetime.fromisoformat(start)
            end_date = datetime.fromisoformat(end)

            # Ensure dates are timezone aware
            if is_naive(start_date):
                start_date = make_aware(start_date)
            if is_naive(end_date):
                end_date = make_aware(end_date)

            # Filter events within the date range
            events = Event.objects.filter(start_time__gte=start_date, end_time__lte=end_date)
            events_list = [
                {
                    'id': event.id,
                    'title': event.title,
                    'start': event.start_time.isoformat(),
                    'end': event.end_time.isoformat() if event.end_time else None,
                } for event in events
            ]
            return JsonResponse(events_list, safe=False)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid date range'}, status=400)


# Landing Page View
def landing_page(request):
    return render(request, 'landing/landing_page.html')

from django.utils.timezone import make_aware, is_naive
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')

        if not title or not start or not end:
            logger.error(f"Missing required data: title={title}, start={start}, end={end}")
            return JsonResponse({'success': False, 'error': 'Missing title, start, or end data'}, status=400)

        try:
            # Handle the 'Z' suffix for UTC time
            if start.endswith('Z'):
                start = start[:-1]  # Remove 'Z' from the end of the string
            if end.endswith('Z'):
                end = end[:-1]  # Remove 'Z' from the end of the string

            # Log the start and end time before conversion
            logger.info(f"Received start={start}, end={end}")

            # Convert start and end to datetime objects
            start_time = datetime.fromisoformat(start)
            end_time = datetime.fromisoformat(end) if end else start_time

            # Ensure that the datetime is timezone-aware
            if is_naive(start_time):
                start_time = make_aware(start_time)
            if is_naive(end_time):
                end_time = make_aware(end_time)

            # Log the converted times
            logger.info(f"Converted start_time={start_time}, end_time={end_time}")

            # Create and save the event
            event = Event.objects.create(title=title, start_time=start_time, end_time=end_time)
            return JsonResponse({'success': True, 'event_id': event.id})
        except Exception as e:
            logger.error(f"Error while creating event: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    logger.error("Invalid request method")
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)


# Edit Event (CSRF exempt for AJAX requests)
from django.utils.timezone import make_aware, is_naive
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def edit_event(request, event_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')

        # Debugging: Check if all required data is present
        if not title or not start:
            logger.error(f"Missing required data: title={title}, start={start}, end={end}")
            return JsonResponse({'success': False, 'error': 'Missing title or start date.'}, status=400)

        try:
            # Remove 'Z' from the ISO string if it exists
            if start.endswith('Z'):
                start = start[:-1]
            if end and end.endswith('Z'):
                end = end[:-1]

            # Debugging: Log received data
            logger.info(f"Received data - Title: {title}, Start: {start}, End: {end}")

            # Fetch the event from the database
            event = Event.objects.get(id=event_id)

            # Update the event title and times
            event.title = title
            event.start_time = datetime.fromisoformat(start)
            event.end_time = datetime.fromisoformat(end) if end else event.start_time

            # Ensure the datetime is timezone-aware
            if is_naive(event.start_time):
                event.start_time = make_aware(event.start_time)
            if is_naive(event.end_time):
                event.end_time = make_aware(event.end_time)

            event.save()  # Save the updated event
            logger.info(f"Event updated successfully: {event.id}")
            return JsonResponse({'success': True})
        except Event.DoesNotExist:
            logger.error(f"Event not found: {event_id}")
            return JsonResponse({'success': False, 'error': 'Event not found.'}, status=404)
        except Exception as e:
            logger.error(f"Error while updating event: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    logger.error("Invalid request method")
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)


# Delete Event (CSRF exempt for AJAX requests)
@csrf_exempt
def delete_event(request, event_id):
    if request.method == 'POST':
        try:
            # Find the event by ID and delete it
            event = Event.objects.get(id=event_id)
            event.delete()
            return JsonResponse({'success': True})
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
