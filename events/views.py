# from django.shortcuts import render
# from datetime import datetime
#
# from django.views.decorators.csrf import csrf_exempt
#
# from .models import Event
# from django.http import JsonResponse
#
# def calendar_view(request, year=None, month=None):
#     if not year:
#         year = datetime.now().year
#     if not month:
#         month = datetime.now().month
#
#     # Optionally, filter events based on the selected year and month
#     events = Event.objects.filter(start_time__year=year, start_time__month=month)
#
#     # Render the template and pass events to be displayed by FullCalendar
#     return render(request, 'events/calendar.html', {'year': year, 'month': month})
#
# def home_view(request):
#     return render(request, 'events/home.html')
#
# from django.http import JsonResponse
# from .models import Event  # Assuming you have an Event model
#
# def calendar_events(request):
#     events = Event.objects.all()
#     events_data = []
#     for event in events:
#         events_data.append({
#             'title': event.title,
#             'start': event.start_date.isoformat(),
#             'end': event.end_date.isoformat() if event.end_date else None,
#         })
#     return JsonResponse(events_data, safe=False)
#
# from django.http import JsonResponse
# from .models import Event
# from datetime import datetime
# from django.views.decorators.csrf import csrf_exempt
#
# def events_json(request, year, month):
#     events = Event.objects.filter(start_time__year=year, start_time__month=month)
#     events_list = []
#     for event in events:
#         events_list.append({
#             'title': event.title,
#             'start': event.start_time.isoformat(),
#             'end': event.end_time.isoformat() if event.end_time else None,
#         })
#     return JsonResponse(events_list, safe=False)
#
# @csrf_exempt
# def add_event(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         start = request.POST.get('start')
#         end = request.POST.get('end')
#
#         # Convert start and end to datetime objects
#         start_time = datetime.fromisoformat(start)
#         end_time = datetime.fromisoformat(end) if end else start_time
#
#         # Create and save the event
#         event = Event(title=title, start_time=start_time, end_time=end_time)
#         event.save()
#
#         return JsonResponse({'success': True})
#
#     return JsonResponse({'success': False}, status=400)
#
# from django.shortcuts import render
#
# def landing_page(request):
#     return render(request, 'landing/landing_page.html')

from django.shortcuts import render

def calendar_view(request, year=None, month=None):
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month

    # Optionally, filter events based on the selected year and month
    events = Event.objects.filter(start_time__year=year, start_time__month=month)

    # Render the template and pass events to be displayed by FullCalendar
    return render(request, 'events/calendar.html', {'year': year, 'month': month, 'events': events})


from django.http import JsonResponse
from django.utils.timezone import make_aware, is_naive
from datetime import datetime


def events_json(request):
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)

    if start and end:
        # Convert strings to datetime objects
        start_date = datetime.fromisoformat(start)
        end_date = datetime.fromisoformat(end)

        # Only make datetime aware if it is naive
        if is_naive(start_date):
            start_date = make_aware(start_date)
        if is_naive(end_date):
            end_date = make_aware(end_date)

        # Filter events in the date range
        events = Event.objects.filter(start_time__gte=start_date, end_time__lte=end_date)
        events_list = []
        for event in events:
            events_list.append({
                'id': event.id,  # Include the event ID so FullCalendar can reference it
                'title': event.title,
                'start': event.start_time.isoformat(),
                'end': event.end_time.isoformat() if event.end_time else None,
            })
        return JsonResponse(events_list, safe=False)

    return JsonResponse({'error': 'Invalid date range'}, status=400)


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import datetime
from .models import Event

from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing/landing_page.html')  # Point to your landing page template


@csrf_exempt
def add_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')

        try:
            # Convert start and end to datetime objects
            start_time = datetime.fromisoformat(start)
            end_time = datetime.fromisoformat(end) if end else start_time

            # Create and save the event
            event = Event.objects.create(title=title, start_time=start_time, end_time=end_time)
            return JsonResponse({'success': True, 'event_id': event.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@csrf_exempt
def edit_event(request, event_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        start = request.POST.get('start')
        end = request.POST.get('end')

        try:
            # Convert start and end to datetime objects
            start_time = datetime.fromisoformat(start)
            end_time = datetime.fromisoformat(end) if end else start_time

            # Find the event and update it
            event = Event.objects.get(id=event_id)
            event.title = title
            event.start_time = start_time
            event.end_time = end_time
            event.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@csrf_exempt
def delete_event(request, event_id):
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return JsonResponse({'success': True})
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)
