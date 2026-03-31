from django.db import models


class AuditLog(models.Model):
    actor_username = models.CharField(max_length=150)
    actor_ip = models.GenericIPAddressField(null=True, blank=True)
    action = models.CharField(max_length=128)
    object_type = models.CharField(max_length=120)
    object_id = models.CharField(max_length=120)
    metadata = models.JSONField(default=dict, blank=True)
    event_hash = models.CharField(max_length=64)
    signature = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
