from rest_framework import serializers
from .models import SecureMessage, SharedEvidence, WorkspaceNote


class WorkspaceNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkspaceNote
        fields = '__all__'


class SecureMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureMessage
        fields = '__all__'


class SharedEvidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedEvidence
        fields = '__all__'
