from apps.core.viewmixins import AuditedSecureModelViewSet
from .models import Geofence, GeospatialAlert, IncidentLocation
from .serializers import GeofenceSerializer, GeospatialAlertSerializer, IncidentLocationSerializer


class IncidentLocationViewSet(AuditedSecureModelViewSet):
    queryset = IncidentLocation.objects.all().order_by('-occurred_at')
    serializer_class = IncidentLocationSerializer


class GeofenceViewSet(AuditedSecureModelViewSet):
    queryset = Geofence.objects.all().order_by('name')
    serializer_class = GeofenceSerializer


class GeospatialAlertViewSet(AuditedSecureModelViewSet):
    queryset = GeospatialAlert.objects.select_related('geofence', 'incident').all().order_by('-created_at')
    serializer_class = GeospatialAlertSerializer
