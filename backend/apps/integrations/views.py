import json
from django.http import HttpResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from apps.audit.services import record_audit_event
from apps.geo.models import IncidentLocation
from .adapters import compute_sha256, normalize_forensic_payload
from apps.forensics.models import ForensicIngestion, ForensicTask


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def forensic_ingest(request):
    task_id = request.data.get('task_id')
    raw_payload = request.data.get('payload', {})
    task = ForensicTask.objects.filter(id=task_id).first()
    if not task:
        return Response({'detail': 'task not found'}, status=status.HTTP_404_NOT_FOUND)

    normalized = normalize_forensic_payload(raw_payload)
    payload_str = json.dumps(normalized, sort_keys=True)
    ingestion = ForensicIngestion.objects.create(
        task=task,
        source_system=normalized['source'],
        payload_format='JSON',
        payload=normalized,
        sha256=compute_sha256(payload_str),
    )
    record_audit_event(request.user.username, request.META.get('REMOTE_ADDR'), 'forensic_ingest', 'ForensicIngestion', str(ingestion.id))
    return Response({'id': ingestion.id, 'sha256': ingestion.sha256})


@api_view(['POST'])
@permission_classes([AllowAny])
def africastalking_ussd(request):
    session_id = request.data.get('sessionId')
    text = request.data.get('text', '')
    phone_number = request.data.get('phoneNumber', '')

    if text == '':
        response = 'CON SentinelKE Citizen Channel\n1. Report threat\n2. Missing person\n3. Emergency alert'
    else:
        choice = text.split('*')[0]
        description = {'1': 'threat report', '2': 'missing person', '3': 'emergency alert'}.get(choice, 'general report')
        IncidentLocation.objects.create(
            description=f'USSD {description} from {phone_number}',
            location='POINT(36.8219 -1.2921)',
            occurred_at=timezone.now(),
        )
        response = 'END Report received. Reference queued for analyst review.'

    if session_id:
        record_audit_event('ussd_gateway', request.META.get('REMOTE_ADDR'), 'ussd_submission', 'USSDSession', session_id, {'phone': phone_number})

    return HttpResponse(response, content_type='text/plain')
