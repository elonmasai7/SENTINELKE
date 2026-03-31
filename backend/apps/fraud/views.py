from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.viewmixins import AuditedSecureModelViewSet
from .models import FinancialTransaction, FraudAlert
from .serializers import FinancialTransactionSerializer, FraudAlertSerializer


class FinancialTransactionViewSet(AuditedSecureModelViewSet):
    queryset = FinancialTransaction.objects.all().order_by('-occurred_at')
    serializer_class = FinancialTransactionSerializer

    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        tx = self.get_object()
        risk_score = 0.9 if tx.amount > 1000000 else 0.35
        reason = 'High-value transfer anomaly' if tx.amount > 1000000 else 'Baseline monitoring event'
        alert = FraudAlert.objects.create(transaction=tx, risk_score=risk_score, reason=reason)
        self._audit('analyze', alert)
        return Response(FraudAlertSerializer(alert).data)


class FraudAlertViewSet(AuditedSecureModelViewSet):
    queryset = FraudAlert.objects.select_related('transaction').all().order_by('-created_at')
    serializer_class = FraudAlertSerializer
