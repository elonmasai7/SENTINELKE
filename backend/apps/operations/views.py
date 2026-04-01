from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.compliance.services import enforce_warrant_scope
from apps.core.viewmixins import AuditedSecureModelViewSet

from .models import AROverlayPacket, JointTaskWorkspace, LiveAssetPosition, TranscriptRecord, WorkspaceComment
from .serializers import (
    AROverlayPacketSerializer,
    JointTaskWorkspaceSerializer,
    LiveAssetPositionSerializer,
    TranscriptRecordSerializer,
    WorkspaceCommentSerializer,
)


class LiveAssetPositionViewSet(AuditedSecureModelViewSet):
    queryset = LiveAssetPosition.objects.select_related('case').all().order_by('-observed_at')
    serializer_class = LiveAssetPositionSerializer

    def perform_create(self, serializer):
        obj = serializer.save()
        self._audit('create', obj)
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                'operations_live',
                {
                    'type': 'operations.update',
                    'payload': {
                        'event': 'live_position',
                        **LiveAssetPositionSerializer(obj).data,
                    },
                },
            )


class AROverlayPacketViewSet(AuditedSecureModelViewSet):
    queryset = AROverlayPacket.objects.select_related('case', 'warrant', 'created_by').all().order_by('-created_at')
    serializer_class = AROverlayPacketSerializer

    def perform_create(self, serializer):
        case = serializer.validated_data['case']
        warrant = serializer.validated_data['warrant']
        enforce_warrant_scope(warrant=warrant, case=case, requested_scope=serializer.validated_data.get('requested_scope', {}))
        super().perform_create(serializer)


class TranscriptRecordViewSet(AuditedSecureModelViewSet):
    queryset = TranscriptRecord.objects.select_related('case', 'warrant', 'created_by').all().order_by('-created_at')
    serializer_class = TranscriptRecordSerializer

    def perform_create(self, serializer):
        case = serializer.validated_data['case']
        warrant = serializer.validated_data['warrant']
        enforce_warrant_scope(warrant=warrant, case=case, requested_scope=serializer.validated_data.get('requested_scope', {}))
        super().perform_create(serializer)


class JointTaskWorkspaceViewSet(AuditedSecureModelViewSet):
    queryset = JointTaskWorkspace.objects.select_related('case', 'created_by').all().order_by('-created_at')
    serializer_class = JointTaskWorkspaceSerializer

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        workspace = self.get_object()
        comments = workspace.comments.select_related('author').all().order_by('-created_at')[:50]
        return Response(WorkspaceCommentSerializer(comments, many=True).data)


class WorkspaceCommentViewSet(AuditedSecureModelViewSet):
    queryset = WorkspaceComment.objects.select_related('workspace', 'author').all().order_by('-created_at')
    serializer_class = WorkspaceCommentSerializer
