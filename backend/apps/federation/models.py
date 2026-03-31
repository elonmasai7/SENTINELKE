from django.db import models
from django.contrib.auth import get_user_model

from apps.compliance.models import Warrant
from apps.core.models import Case

User = get_user_model()


class FederatedQuery(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='federated_queries')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    query_text = models.TextField()
    partner_systems = models.JSONField(default=list)
    selective_visibility = models.JSONField(default=dict, blank=True)
    requested_scope = models.JSONField(default=dict, blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class FederatedResult(models.Model):
    query = models.ForeignKey(FederatedQuery, on_delete=models.CASCADE, related_name='results')
    partner = models.CharField(max_length=120)
    result_reference = models.CharField(max_length=255)
    relevance = models.FloatField(default=0.0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InternationalPartnerExchange(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='international_exchanges')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    partner = models.CharField(max_length=120)
    endpoint = models.CharField(max_length=255)
    consent_reference = models.CharField(max_length=255)
    response_status = models.PositiveIntegerField(default=0)
    payload_hash = models.CharField(max_length=64)
    requested_scope = models.JSONField(default=dict, blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
