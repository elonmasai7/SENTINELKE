from django.contrib import admin
from django.urls import include, path
from apps.core.views import dashboard_home, static_health

urlpatterns = [
    path('', dashboard_home, name='dashboard-home'),
    path('system/static-health/', static_health, name='static-health'),
    path('admin/', admin.site.urls),
    path('api/core/', include('apps.core.urls')),
    path('api/audit/', include('apps.audit.urls')),
    path('api/compliance/', include('apps.compliance.urls')),
    path('api/forensics/', include('apps.forensics.urls')),
    path('api/intelligence/', include('apps.intelligence.urls')),
    path('api/fraud/', include('apps.fraud.urls')),
    path('api/geo/', include('apps.geo.urls')),
    path('api/surveillance/', include('apps.surveillance.urls')),
    path('api/collaboration/', include('apps.collaboration.urls')),
    path('api/integrations/', include('apps.integrations.urls')),
    path('api/ai-intelligence/', include('apps.ai_intelligence.urls')),
    path('api/operations/', include('apps.operations.urls')),
    path('api/forensics-advanced/', include('apps.forensics_advanced.urls')),
    path('api/biometrics/', include('apps.biometrics.urls')),
    path('api/evidence-automation/', include('apps.evidence_automation.urls')),
    path('api/field-ops/', include('apps.field_ops.urls')),
    path('api/federation/', include('apps.federation.urls')),
    path('api/ai/', include('apps.ai_gateway.urls')),
]

