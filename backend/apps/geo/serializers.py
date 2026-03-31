from rest_framework import serializers
from .models import Geofence, GeospatialAlert, IncidentLocation


class IncidentLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = IncidentLocation
        fields = '__all__'


class GeofenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Geofence
        fields = '__all__'


class GeospatialAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeospatialAlert
        fields = '__all__'
