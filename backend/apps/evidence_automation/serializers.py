from rest_framework import serializers

from .models import AutomatedForensicReport, EvidenceIntegrityAnchor, WitnessRedactionJob


class EvidenceIntegrityAnchorSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvidenceIntegrityAnchor
        fields = '__all__'


class AutomatedForensicReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AutomatedForensicReport
        fields = '__all__'


class WitnessRedactionJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = WitnessRedactionJob
        fields = '__all__'
