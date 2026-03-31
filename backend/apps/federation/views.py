from apps.compliance.services import enforce_warrant_scope
from apps.core.viewmixins import AuditedSecureModelViewSet

from .models import FederatedQuery, FederatedResult, InternationalPartnerExchange
from .serializers import FederatedQuerySerializer, FederatedResultSerializer, InternationalPartnerExchangeSerializer


class FederatedQueryViewSet(AuditedSecureModelViewSet):
    queryset = FederatedQuery.objects.select_related('case', 'warrant', 'requested_by').all().order_by('-created_at')
    serializer_class = FederatedQuerySerializer

    def perform_create(self, serializer):
        case = serializer.validated_data['case']
        warrant = serializer.validated_data['warrant']
        enforce_warrant_scope(warrant=warrant, case=case, requested_scope=serializer.validated_data.get('requested_scope', {}))
        super().perform_create(serializer)


class FederatedResultViewSet(AuditedSecureModelViewSet):
    queryset = FederatedResult.objects.select_related('query').all().order_by('-created_at')
    serializer_class = FederatedResultSerializer


class InternationalPartnerExchangeViewSet(AuditedSecureModelViewSet):
    queryset = InternationalPartnerExchange.objects.select_related('case', 'warrant', 'requested_by').all().order_by('-created_at')
    serializer_class = InternationalPartnerExchangeSerializer

    def perform_create(self, serializer):
        case = serializer.validated_data['case']
        warrant = serializer.validated_data['warrant']
        enforce_warrant_scope(warrant=warrant, case=case, requested_scope=serializer.validated_data.get('requested_scope', {}))
        super().perform_create(serializer)
