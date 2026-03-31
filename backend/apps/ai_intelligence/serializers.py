from rest_framework import serializers

from .models import AISummary, PatternOfLifeProfile, PredictiveThreatScore, SyntheticMediaScan


class PatternOfLifeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatternOfLifeProfile
        fields = '__all__'


class PredictiveThreatScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictiveThreatScore
        fields = '__all__'


class AISummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = AISummary
        fields = '__all__'


class SyntheticMediaScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyntheticMediaScan
        fields = '__all__'
