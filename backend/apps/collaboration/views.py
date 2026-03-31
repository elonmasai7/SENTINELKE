from apps.core.viewmixins import AuditedSecureModelViewSet
from .models import SecureMessage, SharedEvidence, WorkspaceNote
from .serializers import SecureMessageSerializer, SharedEvidenceSerializer, WorkspaceNoteSerializer


class WorkspaceNoteViewSet(AuditedSecureModelViewSet):
    queryset = WorkspaceNote.objects.select_related('case', 'author').all().order_by('-created_at')
    serializer_class = WorkspaceNoteSerializer


class SecureMessageViewSet(AuditedSecureModelViewSet):
    queryset = SecureMessage.objects.select_related('sender', 'receiver').all().order_by('-created_at')
    serializer_class = SecureMessageSerializer


class SharedEvidenceViewSet(AuditedSecureModelViewSet):
    queryset = SharedEvidence.objects.select_related('case', 'shared_by').all().order_by('-created_at')
    serializer_class = SharedEvidenceSerializer
