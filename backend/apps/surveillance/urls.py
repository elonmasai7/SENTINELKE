from rest_framework.routers import DefaultRouter
from .views import InterceptMetadataRecordViewSet, SurveillanceRequestViewSet

router = DefaultRouter()
router.register(r'requests', SurveillanceRequestViewSet)
router.register(r'intercept-metadata', InterceptMetadataRecordViewSet)

urlpatterns = router.urls
