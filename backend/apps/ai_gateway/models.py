import hashlib

from django.conf import settings
from django.db import models

from apps.compliance.models import Warrant
from apps.core.models import Case


class AIRequestLog(models.Model):
    class SensitivityLevel(models.TextChoices):
        PUBLIC = 'public', 'Public'
        RESTRICTED = 'restricted', 'Restricted'
        CLASSIFIED = 'classified', 'Classified'

    class ApprovalStatus(models.TextChoices):
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        PENDING = 'PENDING', 'Pending'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    case = models.ForeignKey(Case, on_delete=models.PROTECT, null=True, blank=True)
    provider_used = models.CharField(max_length=64)
    task_type = models.CharField(max_length=64)
    prompt_hash = models.CharField(max_length=64)
    response_hash = models.CharField(max_length=64)
    sensitivity_level = models.CharField(max_length=16, choices=SensitivityLevel.choices)
    action_reason = models.CharField(max_length=255, blank=True)
    warrant_reference = models.ForeignKey(Warrant, on_delete=models.PROTECT, null=True, blank=True)
    approval_status = models.CharField(max_length=16, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    prompt_tokens = models.PositiveIntegerField(default=0)
    response_tokens = models.PositiveIntegerField(default=0)
    total_tokens = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']


class AIResponseCache(models.Model):
    task_type = models.CharField(max_length=64)
    provider_used = models.CharField(max_length=64)
    prompt_hash = models.CharField(max_length=64, unique=True)
    response_body = models.JSONField(default=dict)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['task_type', 'provider_used'])]


def stable_hash(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()
