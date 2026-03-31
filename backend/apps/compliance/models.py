from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import Case

User = get_user_model()


class Warrant(models.Model):
    class WarrantStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        ACTIVE = 'ACTIVE', 'Active'
        EXPIRED = 'EXPIRED', 'Expired'
        REJECTED = 'REJECTED', 'Rejected'

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='warrants')
    warrant_number = models.CharField(max_length=80, unique=True)
    issuing_court = models.CharField(max_length=255)
    issued_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    status = models.CharField(max_length=16, choices=WarrantStatus.choices, default=WarrantStatus.DRAFT)
    document_path = models.CharField(max_length=500)
    authorized_scope = models.JSONField(default=dict, blank=True)
    proportionality_notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class ApprovalRecord(models.Model):
    class ApprovalDecision(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    warrant = models.ForeignKey(Warrant, on_delete=models.CASCADE, related_name='approvals')
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT)
    decision = models.CharField(max_length=16, choices=ApprovalDecision.choices, default=ApprovalDecision.PENDING)
    comment = models.TextField(blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)


class RetentionPolicy(models.Model):
    scope = models.CharField(max_length=64, unique=True)
    retention_days = models.PositiveIntegerField(default=365)
    auto_delete = models.BooleanField(default=True)
    enabled = models.BooleanField(default=True)
