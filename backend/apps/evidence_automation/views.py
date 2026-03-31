from apps.compliance.services import enforce_warrant_scope
from apps.core.viewmixins import AuditedSecureModelViewSet

from .blockchain import anchor_hash
from .models import AutomatedForensicReport, EvidenceIntegrityAnchor, WitnessRedactionJob
from .serializers import AutomatedForensicReportSerializer, EvidenceIntegrityAnchorSerializer, WitnessRedactionJobSerializer


class EvidenceIntegrityAnchorViewSet(AuditedSecureModelViewSet):
    queryset = EvidenceIntegrityAnchor.objects.select_related('case', 'officer').all().order_by('-anchored_at')
    serializer_class = EvidenceIntegrityAnchorSerializer

    def perform_create(self, serializer):
        obj = serializer.save()
        obj.ledger_reference = anchor_hash(obj.evidence_hash, str(obj.case_id), str(obj.officer_id))
        obj.save(update_fields=['ledger_reference'])
        self._audit('anchor', obj)


class AutomatedForensicReportViewSet(AuditedSecureModelViewSet):
    queryset = AutomatedForensicReport.objects.select_related('case', 'warrant', 'generated_by').all().order_by('-created_at')
    serializer_class = AutomatedForensicReportSerializer

    def perform_create(self, serializer):
        case = serializer.validated_data['case']
        warrant = serializer.validated_data['warrant']
        enforce_warrant_scope(warrant=warrant, case=case, requested_scope=serializer.validated_data.get('requested_scope', {}))
        super().perform_create(serializer)


class WitnessRedactionJobViewSet(AuditedSecureModelViewSet):
    queryset = WitnessRedactionJob.objects.select_related('case', 'warrant', 'created_by').all().order_by('-created_at')
    serializer_class = WitnessRedactionJobSerializer

    def perform_create(self, serializer):
        case = serializer.validated_data['case']
        warrant = serializer.validated_data['warrant']
        enforce_warrant_scope(warrant=warrant, case=case, requested_scope=serializer.validated_data.get('requested_scope', {}))
        super().perform_create(serializer)
