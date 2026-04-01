from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import AgencyViewSet, CaseViewSet, UserProfileViewSet, dashboard_live_feed

router = DefaultRouter()
router.register(r'agencies', AgencyViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'cases', CaseViewSet)

urlpatterns = [
    path('dashboard/live-feed/', dashboard_live_feed, name='dashboard-live-feed'),
] + router.urls
