from django.shortcuts import render
from datetime import datetime

from django.views.decorators.csrf import csrf_exempt

from .models import Event
from django.http import JsonResponse

def calendar_view(request, year=None, month=None):
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month

    # Optionally, filter events based on the selected year and month
    events = Event.objects.filter(start_time__year=year, start_time__month=month)

    # Render the template and pass events to be displayed by FullCalendar
    return render(request, 'events/calendar.html', {'year': year, 'month': month})

def home_view(request):
    return render(request, 'events/home.html')

from django.http import JsonResponse
from .models import Event  # Assuming you have an Event model

def calendar_events(request):
    events = Event.objects.all()
    events_data = []
    for event in events:
        events_data.append({
            'title': event.title,
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat() if event.end_date else None,
        })
    return JsonResponse(events_data, safe=False)

from django.http import JsonResponse
from .models import Event
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

def events_json(request, year, month):
    events = Event.objects.filter(start_time__year=year, start_time__month=month)
    events_list = []
    for event in events:
        events_list.append({
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat() if event.end_time else None,
        })
    return JsonResponse(events_list, safe=False)

@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')

        # Convert start and end to datetime objects
        start_time = datetime.fromisoformat(start)
        end_time = datetime.fromisoformat(end) if end else start_time

        # Create and save the event
        event = Event(title=title, start_time=start_time, end_time=end_time)
        event.save()

        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)
