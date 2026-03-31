from rest_framework import serializers

from .models import CloudLegalHold, CryptoLedgerEvent, IoTForensicArtifact, WalletCluster


class WalletClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletCluster
        fields = '__all__'


class CryptoLedgerEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoLedgerEvent
        fields = '__all__'


class IoTForensicArtifactSerializer(serializers.ModelSerializer):
    class Meta:
        model = IoTForensicArtifact
        fields = '__all__'


class CloudLegalHoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CloudLegalHold
        fields = '__all__'
