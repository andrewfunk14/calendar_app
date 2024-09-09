from django.contrib import admin
from django.urls import path, include
from events import views as event_views  # Import the views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', event_views.landing_page, name='landing_page'),  # Root URL shows the landing page
    path('calendar/', include('events.urls')),  # Calendar-related URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication (login/logout)
]


