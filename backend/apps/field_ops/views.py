from apps.core.viewmixins import AuditedSecureModelViewSet

from .models import DroneFeed, OfflineSyncIntegrityLog
from .serializers import DroneFeedSerializer, OfflineSyncIntegrityLogSerializer


class DroneFeedViewSet(AuditedSecureModelViewSet):
    queryset = DroneFeed.objects.select_related('case').all().order_by('-last_seen')
    serializer_class = DroneFeedSerializer


class OfflineSyncIntegrityLogViewSet(AuditedSecureModelViewSet):
    queryset = OfflineSyncIntegrityLog.objects.select_related('case').all().order_by('-queued_at')
    serializer_class = OfflineSyncIntegrityLogSerializer
