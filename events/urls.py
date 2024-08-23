from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('calendar/<int:year>/<int:month>/', views.calendar_view, name='calendar'),
    path('events/json/<int:year>/<int:month>/', views.events_json, name='events_json'),  # JSON events URL
    path('events/add/', views.add_event, name='add_event'),  # URL for adding events
]




