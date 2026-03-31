from rest_framework import serializers

from .models import AROverlayPacket, JointTaskWorkspace, LiveAssetPosition, TranscriptRecord, WorkspaceComment


class LiveAssetPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiveAssetPosition
        fields = '__all__'


class AROverlayPacketSerializer(serializers.ModelSerializer):
    class Meta:
        model = AROverlayPacket
        fields = '__all__'


class TranscriptRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptRecord
        fields = '__all__'


class JointTaskWorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JointTaskWorkspace
        fields = '__all__'


class WorkspaceCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceComment
        fields = '__all__'
