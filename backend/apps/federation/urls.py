from rest_framework.routers import DefaultRouter

from .views import FederatedQueryViewSet, FederatedResultViewSet, InternationalPartnerExchangeViewSet

router = DefaultRouter()
router.register(r'queries', FederatedQueryViewSet)
router.register(r'results', FederatedResultViewSet)
router.register(r'international-exchanges', InternationalPartnerExchangeViewSet)

urlpatterns = router.urls
