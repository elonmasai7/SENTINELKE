from apps.compliance.services import enforce_warrant_scope
from apps.core.viewmixins import AuditedSecureModelViewSet

from .models import BehavioralBiometricProfile, BiometricFusionQuery
from .serializers import BehavioralBiometricProfileSerializer, BiometricFusionQuerySerializer


class BiometricFusionQueryViewSet(AuditedSecureModelViewSet):
    queryset = BiometricFusionQuery.objects.select_related('case', 'warrant', 'queried_by').all().order_by('-created_at')
    serializer_class = BiometricFusionQuerySerializer

    def perform_create(self, serializer):
        case = serializer.validated_data['case']
        warrant = serializer.validated_data['warrant']
        enforce_warrant_scope(warrant=warrant, case=case, requested_scope=serializer.validated_data.get('requested_scope', {}))
        super().perform_create(serializer)


class BehavioralBiometricProfileViewSet(AuditedSecureModelViewSet):
    queryset = BehavioralBiometricProfile.objects.select_related('profile__user', 'profile__agency').all().order_by('-last_validated_at')
    serializer_class = BehavioralBiometricProfileSerializer
