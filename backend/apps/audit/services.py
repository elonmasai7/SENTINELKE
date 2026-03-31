import hashlib
import hmac
import json
from django.conf import settings
from .models import AuditLog


def _canonical_payload(payload: dict) -> str:
    return json.dumps(payload, sort_keys=True, separators=(',', ':'))


def record_audit_event(actor_username: str, actor_ip: str, action: str, object_type: str, object_id: str, metadata: dict | None = None) -> AuditLog:
    metadata = metadata or {}
    payload = {
        'actor_username': actor_username,
        'actor_ip': actor_ip,
        'action': action,
        'object_type': object_type,
        'object_id': object_id,
        'metadata': metadata,
    }
    canonical = _canonical_payload(payload)
    event_hash = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    signature = hmac.new(
        key=settings.AUDIT_SIGNING_KEY.encode('utf-8'),
        msg=event_hash.encode('utf-8'),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return AuditLog.objects.create(
        actor_username=actor_username,
        actor_ip=actor_ip,
        action=action,
        object_type=object_type,
        object_id=object_id,
        metadata=metadata,
        event_hash=event_hash,
        signature=signature,
    )
