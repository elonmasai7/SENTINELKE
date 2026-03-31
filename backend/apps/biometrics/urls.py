from rest_framework.routers import DefaultRouter

from .views import BehavioralBiometricProfileViewSet, BiometricFusionQueryViewSet

router = DefaultRouter()
router.register(r'fusion-queries', BiometricFusionQueryViewSet)
router.register(r'behavioral-profiles', BehavioralBiometricProfileViewSet)

urlpatterns = router.urls
