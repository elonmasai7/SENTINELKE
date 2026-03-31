from rest_framework.routers import DefaultRouter
from .views import ApprovalRecordViewSet, RetentionPolicyViewSet, WarrantViewSet

router = DefaultRouter()
router.register(r'warrants', WarrantViewSet)
router.register(r'approvals', ApprovalRecordViewSet)
router.register(r'retention-policies', RetentionPolicyViewSet)

urlpatterns = router.urls
