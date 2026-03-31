from django.contrib import admin
from django.urls import include, path
from apps.core.views import dashboard_home

urlpatterns = [
    path('', dashboard_home, name='dashboard-home'),
    path('admin/', admin.site.urls),
    path('api/core/', include('apps.core.urls')),
    path('api/audit/', include('apps.audit.urls')),
    path('api/compliance/', include('apps.compliance.urls')),
    path('api/forensics/', include('apps.forensics.urls')),
    path('api/intelligence/', include('apps.intelligence.urls')),
    path('api/fraud/', include('apps.fraud.urls')),
    path('api/surveillance/', include('apps.surveillance.urls')),
    path('api/collaboration/', include('apps.collaboration.urls')),
]
