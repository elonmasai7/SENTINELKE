from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import Case
from apps.compliance.models import Warrant

User = get_user_model()


class SurveillanceRequest(models.Model):
    class RequestStatus(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        PENDING = 'PENDING', 'Pending Approval'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        EXECUTED = 'EXECUTED', 'Executed'

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='surveillance_requests')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    target_identifier = models.CharField(max_length=255)
    provider = models.CharField(max_length=120)
    request_metadata = models.JSONField(default=dict)
    status = models.CharField(max_length=16, choices=RequestStatus.choices, default=RequestStatus.DRAFT)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class InterceptMetadataRecord(models.Model):
    surveillance_request = models.ForeignKey(SurveillanceRequest, on_delete=models.CASCADE, related_name='metadata_records')
    provider_reference = models.CharField(max_length=120)
    payload = models.JSONField(default=dict)
    collected_at = models.DateTimeField()
