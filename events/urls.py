# from django.urls import path
# from . import views
#
# urlpatterns = [
#     path('', views.landing_page, name='landing_page'),  # Landing page URL
#     path('calendar/', views.calendar_view, name='calendar'),  # Calendar URL
#     path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar'),  # Calendar with specific year and month
#     path('events/json/<int:year>/<int:month>/', views.events_json, name='events_json'),  # JSON events URL
#     path('events/add/', views.add_event, name='add_event'),  # URL for adding events
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),  # Main calendar page at /calendar/
    path('events/json/', views.events_json, name='events_json'),  # Fetch events JSON data
    path('events/add/', views.add_event, name='add_event'),  # Add event
    path('events/edit/<int:event_id>/', views.edit_event, name='edit_event'),  # Edit event
    path('events/delete/<int:event_id>/', views.delete_event, name='delete_event'),  # Delete event
]



