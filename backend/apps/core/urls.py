from rest_framework.routers import DefaultRouter
from .views import AgencyViewSet, CaseViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'agencies', AgencyViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'cases', CaseViewSet)

urlpatterns = router.urls
