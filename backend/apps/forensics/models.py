from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import Case

User = get_user_model()


class SeizedDevice(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='seized_devices')
    device_tag = models.CharField(max_length=64, unique=True)
    device_type = models.CharField(max_length=64)
    manufacturer = models.CharField(max_length=120, blank=True)
    model = models.CharField(max_length=120, blank=True)
    serial_number = models.CharField(max_length=120, blank=True)
    seized_at = models.DateTimeField()
    seized_by = models.ForeignKey(User, on_delete=models.PROTECT)


class ChainOfCustodyEvent(models.Model):
    device = models.ForeignKey(SeizedDevice, on_delete=models.CASCADE, related_name='custody_events')
    from_actor = models.CharField(max_length=120)
    to_actor = models.CharField(max_length=120)
    event_type = models.CharField(max_length=120)
    notes = models.TextField(blank=True)
    occurred_at = models.DateTimeField()


class ForensicTask(models.Model):
    class TaskStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        RUNNING = 'RUNNING', 'Running'
        COMPLETE = 'COMPLETE', 'Complete'

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='forensic_tasks')
    device = models.ForeignKey(SeizedDevice, on_delete=models.PROTECT, related_name='tasks')
    assigned_lab = models.CharField(max_length=255)
    instructions = models.TextField()
    status = models.CharField(max_length=16, choices=TaskStatus.choices, default=TaskStatus.PENDING)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class ForensicIngestion(models.Model):
    task = models.ForeignKey(ForensicTask, on_delete=models.CASCADE, related_name='ingestions')
    source_system = models.CharField(max_length=120)
    payload_format = models.CharField(max_length=16)
    payload = models.JSONField(default=dict)
    sha256 = models.CharField(max_length=64)
    ingested_at = models.DateTimeField(auto_now_add=True)
