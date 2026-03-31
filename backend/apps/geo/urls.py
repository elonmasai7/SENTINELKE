from rest_framework.routers import DefaultRouter
from .views import GeofenceViewSet, GeospatialAlertViewSet, IncidentLocationViewSet

router = DefaultRouter()
router.register(r'incidents', IncidentLocationViewSet)
router.register(r'geofences', GeofenceViewSet)
router.register(r'alerts', GeospatialAlertViewSet)

urlpatterns = router.urls
