from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.viewmixins import AuditedSecureModelViewSet
from .models import GraphEntity, GraphRelation, IntelReport, ThreatSignal
from .serializers import GraphEntitySerializer, GraphRelationSerializer, IntelReportSerializer, ThreatSignalSerializer

KEYWORDS = {'bomb', 'attack', 'target', 'explosive', 'training'}


def simple_threat_score(text: str) -> float:
    tokens = {t.strip('.,!?;:').lower() for t in text.split()}
    hits = len(tokens.intersection(KEYWORDS))
    return min(1.0, hits / 3.0)


class IntelReportViewSet(AuditedSecureModelViewSet):
    queryset = IntelReport.objects.all().order_by('-reported_at')
    serializer_class = IntelReportSerializer

    @action(detail=True, methods=['post'])
    def score(self, request, pk=None):
        report = self.get_object()
        score = simple_threat_score(report.content)
        signal = ThreatSignal.objects.create(
            report=report,
            label='keyword_risk',
            score=score,
            explanation='Deterministic keyword heuristic for triage.',
        )
        self._audit('score', signal)
        return Response(ThreatSignalSerializer(signal).data)


class ThreatSignalViewSet(AuditedSecureModelViewSet):
    queryset = ThreatSignal.objects.select_related('report').all().order_by('-created_at')
    serializer_class = ThreatSignalSerializer


class GraphEntityViewSet(AuditedSecureModelViewSet):
    queryset = GraphEntity.objects.all().order_by('entity_type')
    serializer_class = GraphEntitySerializer


class GraphRelationViewSet(AuditedSecureModelViewSet):
    queryset = GraphRelation.objects.select_related('from_entity', 'to_entity').all().order_by('-id')
    serializer_class = GraphRelationSerializer
