from rest_framework.routers import DefaultRouter

from .views import DroneFeedViewSet, OfflineSyncIntegrityLogViewSet

router = DefaultRouter()
router.register(r'drone-feeds', DroneFeedViewSet)
router.register(r'offline-sync-logs', OfflineSyncIntegrityLogViewSet)

urlpatterns = router.urls
