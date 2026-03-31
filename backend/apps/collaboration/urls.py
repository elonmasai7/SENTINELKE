from rest_framework.routers import DefaultRouter
from .views import SecureMessageViewSet, SharedEvidenceViewSet, WorkspaceNoteViewSet

router = DefaultRouter()
router.register(r'notes', WorkspaceNoteViewSet)
router.register(r'messages', SecureMessageViewSet)
router.register(r'shared-evidence', SharedEvidenceViewSet)

urlpatterns = router.urls
