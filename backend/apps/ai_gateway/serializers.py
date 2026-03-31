from rest_framework import serializers

from .models import AIRequestLog


class AIRequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIRequestLog
        fields = '__all__'
        read_only_fields = fields


class AIQuerySerializer(serializers.Serializer):
    task_type = serializers.CharField(max_length=64)
    prompt = serializers.CharField()
    sensitivity_level = serializers.ChoiceField(choices=['public', 'restricted', 'classified'])
    case_id = serializers.IntegerField(required=False)
    warrant_id = serializers.IntegerField(required=False)
    action_reason = serializers.CharField(required=False, allow_blank=True)
    use_cache = serializers.BooleanField(required=False, default=True)


class CaseBriefSerializer(serializers.Serializer):
    case_id = serializers.IntegerField()
    sensitivity_level = serializers.ChoiceField(choices=['public', 'restricted', 'classified'])
    warrant_id = serializers.IntegerField(required=False)


class ThreatExplainSerializer(serializers.Serializer):
    entity_id = serializers.CharField(max_length=120)
    sensitivity_level = serializers.ChoiceField(choices=['public', 'restricted', 'classified'])
    case_id = serializers.IntegerField(required=False)
    warrant_id = serializers.IntegerField(required=False)


class VoiceQuerySerializer(serializers.Serializer):
    query = serializers.CharField()
    sensitivity_level = serializers.ChoiceField(choices=['public', 'restricted', 'classified'])
    case_id = serializers.IntegerField(required=False)
    warrant_id = serializers.IntegerField(required=False)


class SummarizeSerializer(serializers.Serializer):
    report_text = serializers.CharField()
    sensitivity_level = serializers.ChoiceField(choices=['public', 'restricted', 'classified'])
    case_id = serializers.IntegerField(required=False)
    warrant_id = serializers.IntegerField(required=False)
