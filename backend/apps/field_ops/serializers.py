from rest_framework import serializers

from .models import DroneFeed, OfflineSyncIntegrityLog


class DroneFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DroneFeed
        fields = '__all__'


class OfflineSyncIntegrityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineSyncIntegrityLog
        fields = '__all__'
