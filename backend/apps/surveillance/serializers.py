from rest_framework import serializers
from .models import InterceptMetadataRecord, SurveillanceRequest


class SurveillanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveillanceRequest
        fields = '__all__'


class InterceptMetadataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterceptMetadataRecord
        fields = '__all__'
