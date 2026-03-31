from django.contrib.gis.db import models
from django.contrib.auth import get_user_model

from apps.compliance.models import Warrant
from apps.core.models import Case

User = get_user_model()


class LiveAssetPosition(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='live_positions', null=True, blank=True)
    asset_type = models.CharField(max_length=64)
    identifier = models.CharField(max_length=120)
    location = models.PointField(geography=True)
    observed_at = models.DateTimeField()
    threat_overlay = models.JSONField(default=dict, blank=True)


class AROverlayPacket(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='ar_overlays')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    overlay_type = models.CharField(max_length=64)
    target_ref = models.CharField(max_length=255)
    payload = models.JSONField(default=dict)
    requested_scope = models.JSONField(default=dict, blank=True)
    expires_at = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class TranscriptRecord(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='transcripts')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    source_audio_ref = models.CharField(max_length=255)
    language = models.CharField(max_length=32)
    original_transcript = models.TextField()
    translated_transcript = models.TextField(blank=True)
    confidence_score = models.FloatField(default=0.0)
    requested_scope = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class JointTaskWorkspace(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='joint_workspaces')
    name = models.CharField(max_length=255)
    participating_agencies = models.JSONField(default=list)
    access_policy = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class WorkspaceComment(models.Model):
    workspace = models.ForeignKey(JointTaskWorkspace, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
