from django.db import models
from django.contrib.auth import get_user_model

from apps.compliance.models import Warrant
from apps.core.models import Case

User = get_user_model()


class WalletCluster(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='wallet_clusters')
    cluster_label = models.CharField(max_length=120)
    wallets = models.JSONField(default=list)
    risk_score = models.FloatField(default=0.0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CryptoLedgerEvent(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='crypto_events')
    blockchain = models.CharField(max_length=32)
    tx_hash = models.CharField(max_length=255, unique=True)
    wallet_from = models.CharField(max_length=255)
    wallet_to = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=24, decimal_places=8)
    amount_usd = models.DecimalField(max_digits=24, decimal_places=2, default=0)
    occurred_at = models.DateTimeField()
    suspicious_flags = models.JSONField(default=list, blank=True)


class IoTForensicArtifact(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='iot_artifacts')
    device_type = models.CharField(max_length=120)
    firmware_version = models.CharField(max_length=80)
    extracted_logs = models.JSONField(default=list)
    linked_persons = models.JSONField(default=list, blank=True)
    captured_at = models.DateTimeField()


class CloudLegalHold(models.Model):
    class HoldStatus(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        RELEASED = 'RELEASED', 'Released'
        EXPIRED = 'EXPIRED', 'Expired'

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='cloud_legal_holds')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    provider = models.CharField(max_length=64)
    account_reference = models.CharField(max_length=255)
    retention_lock_until = models.DateTimeField()
    status = models.CharField(max_length=16, choices=HoldStatus.choices, default=HoldStatus.ACTIVE)
    deletion_events = models.JSONField(default=list, blank=True)
    requested_scope = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
