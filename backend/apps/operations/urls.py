from rest_framework.routers import DefaultRouter

from .views import AROverlayPacketViewSet, JointTaskWorkspaceViewSet, LiveAssetPositionViewSet, TranscriptRecordViewSet, WorkspaceCommentViewSet

router = DefaultRouter()
router.register(r'live-positions', LiveAssetPositionViewSet)
router.register(r'ar-overlays', AROverlayPacketViewSet)
router.register(r'transcripts', TranscriptRecordViewSet)
router.register(r'workspaces', JointTaskWorkspaceViewSet)
router.register(r'workspace-comments', WorkspaceCommentViewSet)

urlpatterns = router.urls
