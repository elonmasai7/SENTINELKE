from rest_framework.exceptions import ValidationError

from apps.compliance.services import is_warrant_active
from apps.core.viewmixins import AuditedSecureModelViewSet
from .models import InterceptMetadataRecord, SurveillanceRequest
from .serializers import InterceptMetadataRecordSerializer, SurveillanceRequestSerializer


class SurveillanceRequestViewSet(AuditedSecureModelViewSet):
    queryset = SurveillanceRequest.objects.select_related('case', 'warrant', 'created_by').all().order_by('-created_at')
    serializer_class = SurveillanceRequestSerializer

    def perform_create(self, serializer):
        warrant = serializer.validated_data['warrant']
        if not is_warrant_active(warrant):
            raise ValidationError('Surveillance blocked: active warrant required.')
        super().perform_create(serializer)


class InterceptMetadataRecordViewSet(AuditedSecureModelViewSet):
    queryset = InterceptMetadataRecord.objects.select_related('surveillance_request').all().order_by('-collected_at')
    serializer_class = InterceptMetadataRecordSerializer
