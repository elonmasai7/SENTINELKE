from rest_framework import serializers
from .models import GraphEntity, GraphRelation, IntelReport, ThreatSignal


class IntelReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntelReport
        fields = '__all__'


class ThreatSignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreatSignal
        fields = '__all__'


class GraphEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphEntity
        fields = '__all__'


class GraphRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraphRelation
        fields = '__all__'
