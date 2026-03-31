from rest_framework.routers import DefaultRouter
from .views import ChainOfCustodyEventViewSet, ForensicIngestionViewSet, ForensicTaskViewSet, SeizedDeviceViewSet

router = DefaultRouter()
router.register(r'devices', SeizedDeviceViewSet)
router.register(r'custody-events', ChainOfCustodyEventViewSet)
router.register(r'tasks', ForensicTaskViewSet)
router.register(r'ingestions', ForensicIngestionViewSet)

urlpatterns = router.urls
