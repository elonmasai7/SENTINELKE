from rest_framework import serializers
from .models import ApprovalRecord, RetentionPolicy, Warrant


class WarrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warrant
        fields = '__all__'


class ApprovalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalRecord
        fields = '__all__'


class RetentionPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = RetentionPolicy
        fields = '__all__'
