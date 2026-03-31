from datetime import timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.audit.services import record_audit_event
from apps.compliance.models import Warrant
from apps.compliance.services import enforce_warrant_scope
from apps.core.access_control import IsAgencyScopedPermission, user_can_access_case
from apps.core.models import Case

from .models import AIRequestLog, AIResponseCache, stable_hash
from .router import route_prompt, select_provider
from .sensitivity import sanitize_prompt
from .serializers import (
    AIQuerySerializer,
    AIRequestLogSerializer,
    CaseBriefSerializer,
    SummarizeSerializer,
    ThreatExplainSerializer,
    VoiceQuerySerializer,
)
from .services.case_brief import generate_case_brief
from .services.intelligence import summarize_intelligence_report
from .services.threat_explain import explain_threat_score
from .services.voice_query import process_natural_language_query


class AIGatewayBaseView(APIView):
    permission_classes = [IsAuthenticated, IsAgencyScopedPermission]

    def _resolve_case(self, case_id):
        if not case_id:
            return None
        case = Case.objects.filter(id=case_id).first()
        if not case:
            raise ValidationError('Case not found.')
        if not user_can_access_case(self.request.user, case):
            raise PermissionDenied('Access denied for case scope.')
        return case

    def _resolve_warrant(self, warrant_id):
        if not warrant_id:
            return None
        warrant = Warrant.objects.filter(id=warrant_id).first()
        if not warrant:
            raise ValidationError('Warrant not found.')
        return warrant

    def _token_count(self, text: str) -> int:
        return len((text or '').split())

    def _cached_response(self, task_type, provider_used, prompt_hash):
        now = timezone.now()
        cached = AIResponseCache.objects.filter(
            task_type=task_type,
            provider_used=provider_used,
            prompt_hash=prompt_hash,
            expires_at__gt=now,
        ).first()
        return cached.response_body if cached else None

    def _store_cache(self, task_type, provider_used, prompt_hash, response_body):
        AIResponseCache.objects.update_or_create(
            prompt_hash=prompt_hash,
            defaults={
                'task_type': task_type,
                'provider_used': provider_used,
                'response_body': response_body,
                'expires_at': timezone.now() + timedelta(minutes=30),
            },
        )

    def _execute_logged(self, *, task_type, raw_prompt, sensitivity_level, case=None, warrant=None, action_reason=''):
        sanitized_prompt, effective_sensitivity, classified_detected = sanitize_prompt(raw_prompt, sensitivity_level)
        requested_scope = {'operation': task_type}

        if case and warrant:
            enforce_warrant_scope(warrant=warrant, case=case, requested_scope=requested_scope)

        provider_hint = select_provider(task_type=task_type, sensitivity_level=effective_sensitivity)
        prompt_hash = stable_hash(sanitized_prompt)

        cached = self._cached_response(task_type=task_type, provider_used=provider_hint, prompt_hash=prompt_hash)
        if cached is not None:
            result = {'text': cached.get('text', ''), 'raw': cached, 'cached': True}
            provider_used = provider_hint
        else:
            provider_used, result = route_prompt(task_type=task_type, prompt=sanitized_prompt, sensitivity_level=effective_sensitivity)
            self._store_cache(task_type=task_type, provider_used=provider_used, prompt_hash=prompt_hash, response_body=result)

        response_text = result.get('text', '')
        response_hash = stable_hash(response_text)
        prompt_tokens = self._token_count(sanitized_prompt)
        response_tokens = self._token_count(response_text)

        approval_status = AIRequestLog.ApprovalStatus.APPROVED
        if classified_detected and provider_used != 'llama_cpp':
            approval_status = AIRequestLog.ApprovalStatus.REJECTED
            raise ValidationError('Compliance block: classified prompts must use local llama.cpp provider.')

        log = AIRequestLog.objects.create(
            user=self.request.user,
            case=case,
            provider_used=provider_used,
            task_type=task_type,
            prompt_hash=prompt_hash,
            response_hash=response_hash,
            sensitivity_level=effective_sensitivity,
            action_reason=action_reason,
            warrant_reference=warrant,
            approval_status=approval_status,
            prompt_tokens=prompt_tokens,
            response_tokens=response_tokens,
            total_tokens=prompt_tokens + response_tokens,
        )

        record_audit_event(
            actor_username=self.request.user.username,
            actor_ip=self.request.META.get('REMOTE_ADDR'),
            action='ai_query',
            object_type='AIRequestLog',
            object_id=str(log.id),
            metadata={'provider': provider_used, 'task_type': task_type, 'sensitivity': effective_sensitivity},
        )

        return {
            'provider_used': provider_used,
            'result': result,
            'effective_sensitivity': effective_sensitivity,
            'token_usage': {
                'prompt_tokens': prompt_tokens,
                'response_tokens': response_tokens,
                'total_tokens': prompt_tokens + response_tokens,
            },
            'log_id': log.id,
        }


class AIQueryView(AIGatewayBaseView):
    def post(self, request):
        serializer = AIQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        case = self._resolve_case(data.get('case_id'))
        warrant = self._resolve_warrant(data.get('warrant_id'))

        payload = self._execute_logged(
            task_type=data['task_type'],
            raw_prompt=data['prompt'],
            sensitivity_level=data['sensitivity_level'],
            case=case,
            warrant=warrant,
            action_reason=data.get('action_reason', ''),
        )
        return Response(payload, status=status.HTTP_200_OK)


class AISummarizeView(AIGatewayBaseView):
    def post(self, request):
        serializer = SummarizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        case = self._resolve_case(data.get('case_id'))
        warrant = self._resolve_warrant(data.get('warrant_id'))

        provider, service_result = summarize_intelligence_report(data['report_text'], data['sensitivity_level'])
        prompt = (
            'Produce executive summary, key suspects, locations, risk indicators, recommended actions. '
            f'Service provider hint: {provider}. Service text: {service_result.get("text", "")}'
        )
        payload = self._execute_logged(
            task_type='strategic_summary',
            raw_prompt=prompt,
            sensitivity_level=data['sensitivity_level'],
            case=case,
            warrant=warrant,
            action_reason='summarize_intelligence_report',
        )
        return Response(payload, status=status.HTTP_200_OK)


class AICaseBriefView(AIGatewayBaseView):
    def post(self, request):
        serializer = CaseBriefSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        case = self._resolve_case(data['case_id'])
        warrant = self._resolve_warrant(data.get('warrant_id'))

        provider, service_result = generate_case_brief(case.id, data['sensitivity_level'])
        prompt = f'Case brief provider hint: {provider}. Draft content: {service_result.get("text", "")}'

        payload = self._execute_logged(
            task_type='legal_brief',
            raw_prompt=prompt,
            sensitivity_level=data['sensitivity_level'],
            case=case,
            warrant=warrant,
            action_reason='generate_case_brief',
        )
        return Response(payload, status=status.HTTP_200_OK)


class AIThreatExplanationView(AIGatewayBaseView):
    def post(self, request):
        serializer = ThreatExplainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        case = self._resolve_case(data.get('case_id'))
        warrant = self._resolve_warrant(data.get('warrant_id'))

        provider, service_result = explain_threat_score(data['entity_id'], sensitivity_level=data['sensitivity_level'])
        prompt = f'Threat explanation provider hint: {provider}. Draft content: {service_result.get("text", "")}'

        payload = self._execute_logged(
            task_type='threat_reasoning',
            raw_prompt=prompt,
            sensitivity_level=data['sensitivity_level'],
            case=case,
            warrant=warrant,
            action_reason='explain_threat_score',
        )
        return Response(payload, status=status.HTTP_200_OK)


class AIVoiceQueryView(AIGatewayBaseView):
    def post(self, request):
        serializer = VoiceQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        case = self._resolve_case(data.get('case_id'))
        warrant = self._resolve_warrant(data.get('warrant_id'))

        processed = process_natural_language_query(data['query'])
        prompt = (
            'Convert this structured query to execution explanation and concise action plan.\n'
            f'Structured Query: {processed["structured_query"]}\n'
            f'Explanation: {processed["explanation"]}'
        )

        payload = self._execute_logged(
            task_type='voice_query',
            raw_prompt=prompt,
            sensitivity_level=data['sensitivity_level'],
            case=case,
            warrant=warrant,
            action_reason='process_natural_language_query',
        )
        payload['structured_query'] = processed['structured_query']
        payload['result_set'] = processed['result_set']
        return Response(payload, status=status.HTTP_200_OK)


class AILogListView(AIGatewayBaseView):
    def get(self, request):
        logs = AIRequestLog.objects.filter(user=request.user).order_by('-created_at')[:200]
        return Response(AIRequestLogSerializer(logs, many=True).data, status=status.HTTP_200_OK)
