from rest_framework.routers import DefaultRouter

from .views import AISummaryViewSet, PatternOfLifeProfileViewSet, PredictiveThreatScoreViewSet, SyntheticMediaScanViewSet

router = DefaultRouter()
router.register(r'pattern-of-life', PatternOfLifeProfileViewSet)
router.register(r'predictive-threat-scores', PredictiveThreatScoreViewSet)
router.register(r'summaries', AISummaryViewSet)
router.register(r'synthetic-media-scans', SyntheticMediaScanViewSet)

urlpatterns = router.urls
