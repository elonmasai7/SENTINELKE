from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.core.access_control import IsAgencyScopedPermission, scope_queryset_for_user
from .models import Agency, Case, UserProfile
from .serializers import AgencySerializer, CaseSerializer, UserProfileSerializer


def dashboard_home(request):
    counts = {
        'cases': Case.objects.count(),
        'agencies': Agency.objects.count(),
    }
    return render(request, 'dashboard/home.html', {'counts': counts})


class ScopedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAgencyScopedPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        return scope_queryset_for_user(queryset, self.request.user)


class AgencyViewSet(ScopedModelViewSet):
    queryset = Agency.objects.all().order_by('name')
    serializer_class = AgencySerializer


class UserProfileViewSet(ScopedModelViewSet):
    queryset = UserProfile.objects.select_related('user', 'agency').all()
    serializer_class = UserProfileSerializer


class CaseViewSet(ScopedModelViewSet):
    queryset = Case.objects.select_related('lead_agency', 'created_by').all().order_by('-created_at')
    serializer_class = CaseSerializer


class AgencyAdminViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.all().order_by('name')
    serializer_class = AgencySerializer
    permission_classes = [IsAdminUser]
