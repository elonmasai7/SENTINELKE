from rest_framework.routers import DefaultRouter
from .views import FinancialTransactionViewSet, FraudAlertViewSet

router = DefaultRouter()
router.register(r'transactions', FinancialTransactionViewSet)
router.register(r'alerts', FraudAlertViewSet)

urlpatterns = router.urls
