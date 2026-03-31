import hashlib
from datetime import datetime


def compute_sha256(payload: str) -> str:
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def normalize_forensic_payload(payload: dict) -> dict:
    return {
        'ingested_at': datetime.utcnow().isoformat() + 'Z',
        'source': payload.get('source', 'unknown'),
        'artifacts': payload.get('artifacts', []),
        'metadata': payload.get('metadata', {}),
    }


def normalize_intercept_metadata(payload: dict) -> dict:
    return {
        'provider_ref': payload.get('provider_ref'),
        'records': payload.get('records', []),
        'lawful_basis': payload.get('lawful_basis'),
    }
