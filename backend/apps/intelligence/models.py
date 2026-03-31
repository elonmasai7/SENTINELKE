from django.db import models
from apps.core.models import Case


class IntelReport(models.Model):
    class SourceType(models.TextChoices):
        OSINT = 'OSINT', 'OSINT'
        HUMINT = 'HUMINT', 'HUMINT'
        SIGINT = 'SIGINT', 'SIGINT'
        CITIZEN = 'CITIZEN', 'Citizen Report'

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='intel_reports', null=True, blank=True)
    source_type = models.CharField(max_length=16, choices=SourceType.choices)
    language = models.CharField(max_length=32, default='en')
    content = models.TextField()
    source_ref = models.CharField(max_length=255, blank=True)
    reported_at = models.DateTimeField()


class ThreatSignal(models.Model):
    report = models.ForeignKey(IntelReport, on_delete=models.CASCADE, related_name='signals')
    label = models.CharField(max_length=120)
    score = models.FloatField(default=0.0)
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class GraphEntity(models.Model):
    entity_type = models.CharField(max_length=64)
    external_id = models.CharField(max_length=120, unique=True)
    properties = models.JSONField(default=dict)


class GraphRelation(models.Model):
    from_entity = models.ForeignKey(GraphEntity, on_delete=models.CASCADE, related_name='outgoing_relations')
    to_entity = models.ForeignKey(GraphEntity, on_delete=models.CASCADE, related_name='incoming_relations')
    relation_type = models.CharField(max_length=64)
    properties = models.JSONField(default=dict)
