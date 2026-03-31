from django.db import models
from django.contrib.auth import get_user_model

from apps.compliance.models import Warrant
from apps.core.models import Case

User = get_user_model()


class EvidenceIntegrityAnchor(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='integrity_anchors')
    evidence_reference = models.CharField(max_length=255)
    evidence_hash = models.CharField(max_length=64)
    officer = models.ForeignKey(User, on_delete=models.PROTECT)
    ledger_reference = models.CharField(max_length=255, blank=True)
    anchored_at = models.DateTimeField(auto_now_add=True)


class AutomatedForensicReport(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='automated_reports')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    generated_by = models.ForeignKey(User, on_delete=models.PROTECT)
    methodology = models.TextField()
    timeline = models.JSONField(default=list, blank=True)
    link_analysis_graph = models.JSONField(default=dict, blank=True)
    pdf_export_path = models.CharField(max_length=500)
    signed_package_path = models.CharField(max_length=500)
    requested_scope = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class WitnessRedactionJob(models.Model):
    class JobStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        RUNNING = 'RUNNING', 'Running'
        COMPLETE = 'COMPLETE', 'Complete'
        FAILED = 'FAILED', 'Failed'

    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='redaction_jobs')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    source_evidence_ref = models.CharField(max_length=255)
    redaction_actions = models.JSONField(default=list)
    output_reference = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=16, choices=JobStatus.choices, default=JobStatus.PENDING)
    requested_scope = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
