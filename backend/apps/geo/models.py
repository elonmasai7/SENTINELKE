from django.contrib.gis.db import models
from apps.core.models import Case


class IncidentLocation(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='incident_locations', null=True, blank=True)
    description = models.CharField(max_length=255)
    location = models.PointField(geography=True)
    occurred_at = models.DateTimeField()


class Geofence(models.Model):
    name = models.CharField(max_length=120)
    zone = models.PolygonField(geography=True)
    active = models.BooleanField(default=True)


class GeospatialAlert(models.Model):
    geofence = models.ForeignKey(Geofence, on_delete=models.CASCADE, related_name='alerts')
    incident = models.ForeignKey(IncidentLocation, on_delete=models.CASCADE, related_name='alerts')
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
