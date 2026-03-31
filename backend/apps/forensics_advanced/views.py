from rest_framework.decorators import action
from rest_framework.response import Response

from apps.compliance.services import enforce_warrant_scope
from apps.core.viewmixins import AuditedSecureModelViewSet

from .models import CloudLegalHold, CryptoLedgerEvent, IoTForensicArtifact, WalletCluster
from .serializers import CloudLegalHoldSerializer, CryptoLedgerEventSerializer, IoTForensicArtifactSerializer, WalletClusterSerializer


class WalletClusterViewSet(AuditedSecureModelViewSet):
    queryset = WalletCluster.objects.select_related('case').all().order_by('-created_at')
    serializer_class = WalletClusterSerializer


class CryptoLedgerEventViewSet(AuditedSecureModelViewSet):
    queryset = CryptoLedgerEvent.objects.select_related('case').all().order_by('-occurred_at')
    serializer_class = CryptoLedgerEventSerializer

    @action(detail=False, methods=['post'])
    def mixer_heuristics(self, request):
        return Response({'heuristic': 'public-ledger-pattern-scan', 'status': 'queued'})


class IoTForensicArtifactViewSet(AuditedSecureModelViewSet):
    queryset = IoTForensicArtifact.objects.select_related('case').all().order_by('-captured_at')
    serializer_class = IoTForensicArtifactSerializer


class CloudLegalHoldViewSet(AuditedSecureModelViewSet):
    queryset = CloudLegalHold.objects.select_related('case', 'warrant', 'created_by').all().order_by('-created_at')
    serializer_class = CloudLegalHoldSerializer

    def perform_create(self, serializer):
        case = serializer.validated_data['case']
        warrant = serializer.validated_data['warrant']
        enforce_warrant_scope(warrant=warrant, case=case, requested_scope=serializer.validated_data.get('requested_scope', {}))
        super().perform_create(serializer)
