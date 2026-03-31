from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import Case

User = get_user_model()


class WorkspaceNote(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    body = models.TextField()
    visibility = models.CharField(max_length=32, default='CASE_TEAM')
    created_at = models.DateTimeField(auto_now_add=True)


class SecureMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.PROTECT, related_name='received_messages')
    ciphertext = models.TextField()
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SharedEvidence(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='shared_evidence')
    shared_by = models.ForeignKey(User, on_delete=models.PROTECT)
    file_path = models.CharField(max_length=500)
    sha256 = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
