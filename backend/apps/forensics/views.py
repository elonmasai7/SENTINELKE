from apps.core.viewmixins import AuditedSecureModelViewSet
from .models import ChainOfCustodyEvent, ForensicIngestion, ForensicTask, SeizedDevice
from .serializers import (
    ChainOfCustodyEventSerializer,
    ForensicIngestionSerializer,
    ForensicTaskSerializer,
    SeizedDeviceSerializer,
)


class SeizedDeviceViewSet(AuditedSecureModelViewSet):
    queryset = SeizedDevice.objects.select_related('case', 'seized_by').all().order_by('-id')
    serializer_class = SeizedDeviceSerializer


class ChainOfCustodyEventViewSet(AuditedSecureModelViewSet):
    queryset = ChainOfCustodyEvent.objects.select_related('device').all().order_by('-occurred_at')
    serializer_class = ChainOfCustodyEventSerializer


class ForensicTaskViewSet(AuditedSecureModelViewSet):
    queryset = ForensicTask.objects.select_related('case', 'device', 'created_by').all().order_by('-created_at')
    serializer_class = ForensicTaskSerializer


class ForensicIngestionViewSet(AuditedSecureModelViewSet):
    queryset = ForensicIngestion.objects.select_related('task').all().order_by('-ingested_at')
    serializer_class = ForensicIngestionSerializer
