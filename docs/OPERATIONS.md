# SentinelKE Operations

## Local Run
1. `cd deployment`
2. `docker compose up --build`
3. Access app at `http://localhost`

## Backend Setup Without Docker
1. Create virtual environment
2. `pip install -r backend/requirements.txt`
3. Set environment variables from `backend/.env.example`
4. `python manage.py migrate`
5. `python manage.py runserver`

## Hardening Checklist
- Replace `DJANGO_SECRET_KEY` and `AUDIT_SIGNING_KEY` with HSM-backed keys.
- Enforce mTLS for agency internal API calls.
- Configure WAF and IP allow-lists.
- Integrate SIEM forwarding for audit streams.
- Enable DB encryption at rest and backup key rotation.
- Restrict admin access to privileged network segments.

## Retention and Deletion
- Define `RetentionPolicy` rows per data domain.
- Run scheduled purge jobs for expired, non-relevant records.
- Preserve legal holds for active judicial orders.

## USSD
- Configure Africa's Talking callback URL to:
  `/api/integrations/ussd/africastalking/`
- Validate source IP allow-list and signed headers at ingress.

## V2 Service Topology
- web: Django ASGI API + templates
- celery-worker: async AI/report/redaction/federation task execution
- edis: broker/result backend/channel layer
- ml-service: FastAPI summarization/synthetic-media/transcription stubs

## Compliance Gate
- For sensitive V2 modules, warrant.authorized_scope is validated against requested operation scope. Out-of-scope requests are blocked at API layer.

- AI gateway endpoints are served under /api/ai/* and require RBAC plus warrant-linked audit context when case-bound.
