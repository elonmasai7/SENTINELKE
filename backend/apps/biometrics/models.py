from django.db import models
from django.contrib.auth import get_user_model

from apps.compliance.models import Warrant
from apps.core.models import Case, UserProfile

User = get_user_model()


class BiometricFusionQuery(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='biometric_queries')
    warrant = models.ForeignKey(Warrant, on_delete=models.PROTECT)
    subject_ref = models.CharField(max_length=255)
    face_embedding_ref = models.CharField(max_length=255, blank=True)
    gait_signature_ref = models.CharField(max_length=255, blank=True)
    voiceprint_ref = models.CharField(max_length=255, blank=True)
    fingerprint_ref = models.CharField(max_length=255, blank=True)
    confidence = models.FloatField(default=0.0)
    decision_support_notes = models.TextField(blank=True)
    requested_scope = models.JSONField(default=dict, blank=True)
    queried_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)


class BehavioralBiometricProfile(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='behavioral_biometrics')
    typing_rhythm = models.JSONField(default=dict, blank=True)
    touchscreen_behavior = models.JSONField(default=dict, blank=True)
    interaction_anomaly_score = models.FloatField(default=0.0)
    last_validated_at = models.DateTimeField(null=True, blank=True)
