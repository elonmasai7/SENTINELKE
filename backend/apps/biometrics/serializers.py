from rest_framework import serializers

from .models import BehavioralBiometricProfile, BiometricFusionQuery


class BiometricFusionQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = BiometricFusionQuery
        fields = '__all__'


class BehavioralBiometricProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BehavioralBiometricProfile
        fields = '__all__'
