# from django.contrib import admin
# from django.urls import path, include
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('events.urls')),  # Use events app for both landing and calendar
#     path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
# ]

from django.contrib import admin
from django.urls import path, include
from events import views as event_views  # For landing page if needed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', event_views.landing_page, name='landing_page'),  # Root URL pointing to landing page
    path('calendar/', include('events.urls')),  # Include all calendar-related URLs under /calendar/
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
]



