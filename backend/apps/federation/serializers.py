from rest_framework import serializers

from .models import FederatedQuery, FederatedResult, InternationalPartnerExchange


class FederatedQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = FederatedQuery
        fields = '__all__'


class FederatedResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = FederatedResult
        fields = '__all__'


class InternationalPartnerExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternationalPartnerExchange
        fields = '__all__'
