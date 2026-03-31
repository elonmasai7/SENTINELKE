from rest_framework.routers import DefaultRouter

from .views import CloudLegalHoldViewSet, CryptoLedgerEventViewSet, IoTForensicArtifactViewSet, WalletClusterViewSet

router = DefaultRouter()
router.register(r'wallet-clusters', WalletClusterViewSet)
router.register(r'crypto-events', CryptoLedgerEventViewSet)
router.register(r'iot-artifacts', IoTForensicArtifactViewSet)
router.register(r'cloud-legal-holds', CloudLegalHoldViewSet)

urlpatterns = router.urls
