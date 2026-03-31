from django.db import models
from django.contrib.auth import get_user_model

from apps.compliance.models import Warrant
from apps.core.models import Case

User = get_user_model()


class PatternOfLifeProfile(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='pattern_profiles')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    subject_ref = models.CharField(max_length=255)
    baseline_window_days = models.PositiveIntegerField(default=30)
    baseline_features = models.JSONField(default=dict)
    deviation_score = models.FloatField(default=0.0)
    anomaly_explanation = models.TextField(blank=True)
    timeline_graph = models.JSONField(default=list, blank=True)
    requested_scope = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class PredictiveThreatScore(models.Model):
    class ThreatLevel(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='predictive_scores')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    subject_ref = models.CharField(max_length=255)
    score = models.PositiveSmallIntegerField()
    level = models.CharField(max_length=16, choices=ThreatLevel.choices)
    explanation = models.TextField()
    factor_breakdown = models.JSONField(default=dict)
    requested_scope = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class AISummary(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='ai_summaries')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    source_type = models.CharField(max_length=64)
    source_reference = models.CharField(max_length=255)
    executive_summary = models.TextField()
    key_entities = models.JSONField(default=list, blank=True)
    named_locations = models.JSONField(default=list, blank=True)
    action_recommendations = models.TextField(blank=True)
    requested_scope = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class SyntheticMediaScan(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='synthetic_scans')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    evidence_ref = models.CharField(max_length=255)
    authenticity_confidence = models.FloatField(default=0.0)
    manipulation_likelihood = models.FloatField(default=0.0)
    flagged_regions = models.JSONField(default=list, blank=True)
    findings = models.JSONField(default=dict, blank=True)
    requested_scope = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
