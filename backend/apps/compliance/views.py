from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from apps.core.viewmixins import AuditedSecureModelViewSet
from .models import ApprovalRecord, RetentionPolicy, Warrant
from .serializers import ApprovalRecordSerializer, RetentionPolicySerializer, WarrantSerializer


class WarrantViewSet(AuditedSecureModelViewSet):
    queryset = Warrant.objects.select_related('case', 'created_by').all().order_by('-created_at')
    serializer_class = WarrantSerializer


class ApprovalRecordViewSet(AuditedSecureModelViewSet):
    queryset = ApprovalRecord.objects.select_related('warrant', 'reviewer').all().order_by('-id')
    serializer_class = ApprovalRecordSerializer


class RetentionPolicyViewSet(viewsets.ModelViewSet):
    queryset = RetentionPolicy.objects.all().order_by('scope')
    serializer_class = RetentionPolicySerializer
    permission_classes = [IsAdminUser]
