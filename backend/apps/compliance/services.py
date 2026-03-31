from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Warrant


def is_warrant_active(warrant: Warrant) -> bool:
    now = timezone.now()
    return warrant.status == Warrant.WarrantStatus.ACTIVE and warrant.issued_at <= now <= warrant.expires_at


def case_has_active_warrant(case) -> bool:
    return any(is_warrant_active(w) for w in case.warrants.all())


def _scope_within_authorization(requested_scope: dict, authorized_scope: dict) -> bool:
    if not authorized_scope:
        return True
    for key, requested in requested_scope.items():
        allowed = authorized_scope.get(key)
        if isinstance(allowed, list):
            if requested not in allowed:
                return False
        elif isinstance(allowed, dict) and isinstance(requested, dict):
            for nested_key, nested_value in requested.items():
                if allowed.get(nested_key) != nested_value:
                    return False
        elif allowed is not None and requested != allowed:
            return False
    return True


def enforce_warrant_scope(*, warrant: Warrant, case, requested_scope: dict | None = None):
    requested_scope = requested_scope or {}
    if warrant.case_id != case.id:
        raise ValidationError('Compliance block: warrant case mismatch.')
    if not is_warrant_active(warrant):
        raise ValidationError('Compliance block: active warrant required.')
    if not _scope_within_authorization(requested_scope, warrant.authorized_scope):
        raise ValidationError('Compliance block: requested operation exceeds warrant scope.')
