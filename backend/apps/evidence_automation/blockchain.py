import hashlib
from datetime import datetime, timezone


def anchor_hash(evidence_hash: str, case_id: str, officer_id: str) -> str:
    payload = f'{evidence_hash}:{case_id}:{officer_id}:{datetime.now(timezone.utc).isoformat()}'
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()
