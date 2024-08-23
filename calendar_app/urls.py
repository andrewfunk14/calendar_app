from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),  # Login URL
    path('calendar/', include('events.urls')),  # Include app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
]


