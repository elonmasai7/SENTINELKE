from rest_framework.routers import DefaultRouter

from .views import AutomatedForensicReportViewSet, EvidenceIntegrityAnchorViewSet, WitnessRedactionJobViewSet

router = DefaultRouter()
router.register(r'integrity-anchors', EvidenceIntegrityAnchorViewSet)
router.register(r'automated-reports', AutomatedForensicReportViewSet)
router.register(r'redaction-jobs', WitnessRedactionJobViewSet)

urlpatterns = router.urls
