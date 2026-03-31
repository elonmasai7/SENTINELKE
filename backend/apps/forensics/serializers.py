from rest_framework import serializers
from .models import ChainOfCustodyEvent, ForensicIngestion, ForensicTask, SeizedDevice


class SeizedDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeizedDevice
        fields = '__all__'


class ChainOfCustodyEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChainOfCustodyEvent
        fields = '__all__'


class ForensicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForensicTask
        fields = '__all__'


class ForensicIngestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForensicIngestion
        fields = '__all__'
