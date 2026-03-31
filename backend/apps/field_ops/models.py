from django.contrib.gis.db import models

from apps.core.models import Case


class DroneFeed(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='drone_feeds', null=True, blank=True)
    feed_identifier = models.CharField(max_length=120, unique=True)
    gps_route = models.LineStringField(geography=True, null=True, blank=True)
    aerial_imagery_reference = models.CharField(max_length=255, blank=True)
    mapping_3d_reference = models.CharField(max_length=255, blank=True)
    last_seen = models.DateTimeField()


class OfflineSyncIntegrityLog(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='offline_sync_logs', null=True, blank=True)
    device_id = models.CharField(max_length=128)
    action_type = models.CharField(max_length=64)
    payload_hash = models.CharField(max_length=64)
    signature = models.CharField(max_length=256)
    queued_at = models.DateTimeField()
    synced_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32, default='QUEUED')
