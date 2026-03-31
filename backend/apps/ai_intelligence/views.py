from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.compliance.services import enforce_warrant_scope
from apps.core.viewmixins import AuditedSecureModelViewSet

from .models import AISummary, PatternOfLifeProfile, PredictiveThreatScore, SyntheticMediaScan
from .serializers import (
    AISummarySerializer,
    PatternOfLifeProfileSerializer,
    PredictiveThreatScoreSerializer,
    SyntheticMediaScanSerializer,
)


class WarrantGatedCreateMixin:
    def perform_create(self, serializer):
        case = serializer.validated_data['case']
        warrant = serializer.validated_data['warrant']
        requested_scope = serializer.validated_data.get('requested_scope', {})
        enforce_warrant_scope(warrant=warrant, case=case, requested_scope=requested_scope)
        super().perform_create(serializer)


class PatternOfLifeProfileViewSet(WarrantGatedCreateMixin, AuditedSecureModelViewSet):
    queryset = PatternOfLifeProfile.objects.select_related('case', 'warrant', 'created_by').all().order_by('-created_at')
    serializer_class = PatternOfLifeProfileSerializer


class PredictiveThreatScoreViewSet(WarrantGatedCreateMixin, AuditedSecureModelViewSet):
    queryset = PredictiveThreatScore.objects.select_related('case', 'warrant', 'created_by').all().order_by('-created_at')
    serializer_class = PredictiveThreatScoreSerializer

    @action(detail=False, methods=['post'])
    def score_subject(self, request):
        factors = request.data.get('factors', {})
        raw = min(100, int(
            factors.get('case_links', 0) * 0.2
            + factors.get('financial_anomalies', 0) * 0.2
            + factors.get('centrality', 0) * 0.2
            + factors.get('language_markers', 0) * 0.15
            + factors.get('travel_deviations', 0) * 0.15
            + factors.get('graph_suspicion', 0) * 0.1
        ))
        if raw >= 85:
            level = 'CRITICAL'
        elif raw >= 70:
            level = 'HIGH'
        elif raw >= 40:
            level = 'MEDIUM'
        else:
            level = 'LOW'
        return Response({'score': raw, 'level': level}, status=status.HTTP_200_OK)


class AISummaryViewSet(WarrantGatedCreateMixin, AuditedSecureModelViewSet):
    queryset = AISummary.objects.select_related('case', 'warrant', 'created_by').all().order_by('-created_at')
    serializer_class = AISummarySerializer


class SyntheticMediaScanViewSet(WarrantGatedCreateMixin, AuditedSecureModelViewSet):
    queryset = SyntheticMediaScan.objects.select_related('case', 'warrant', 'created_by').all().order_by('-created_at')
    serializer_class = SyntheticMediaScanSerializer
