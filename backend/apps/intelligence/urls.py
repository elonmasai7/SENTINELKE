from rest_framework.routers import DefaultRouter
from .views import GraphEntityViewSet, GraphRelationViewSet, IntelReportViewSet, ThreatSignalViewSet

router = DefaultRouter()
router.register(r'reports', IntelReportViewSet)
router.register(r'signals', ThreatSignalViewSet)
router.register(r'graph-entities', GraphEntityViewSet)
router.register(r'graph-relations', GraphRelationViewSet)

urlpatterns = router.urls
