# SentinelKE

SentinelKE is a compliance-first national security and intelligence coordination platform for authorized agencies. This repository provides a production-ready foundation focused on lawful workflows, judicial authorization, and immutable auditability.

## Included Components
- Django + DRF backend with modular security domain apps
- Django template dashboard (Bootstrap 5, no JS frameworks)
- Lawful forensics and intercept integration adapters (API-based)
- USSD intake endpoint for Africa's Talking
- Flutter field kit skeleton (offline queue + secure sync stubs)
- Dockerized deployment with PostGIS, Neo4j, Gunicorn, and Nginx

## Quick Start
1. Copy `backend/.env.example` to `.env` and set production secrets.
2. Start stack:
   - `cd deployment`
   - `docker compose up --build`
3. Create superuser:
   - `docker compose exec web python manage.py createsuperuser`

## Testing
- Use the test settings profile that excludes GIS runtime dependencies:
  - `python backend/manage.py test apps.core.tests apps.compliance.tests --settings=sentinelke.settings_test`

## API Surface (high level)
- `/api/core/` case and agency management
- `/api/compliance/` warrants, approvals, retention
- `/api/forensics/` seized devices, chain-of-custody, ingestion
- `/api/intelligence/` reports, threat scoring, graph entities/relations
- `/api/fraud/` transactions and risk alerts
- `/api/geo/` incidents, geofences, alerts
- `/api/surveillance/` warrant-gated surveillance requests
- `/api/collaboration/` notes, secure messaging, evidence shares
- `/api/integrations/` forensic ingest and USSD callback

## Legal and Safety Posture
- No unlawful exploit capabilities are implemented.
- Sensitive surveillance workflows require active warrant linkage.
- RBAC is enforced by agency scope, assignment, and minimum clearance level.
- Audit records are cryptographically signed and immutable by design.

## Next Engineering Steps
- Extend ABAC policies with purpose-limitation and need-to-know attributes.
- Implement asynchronous ETL pipeline for bulk intelligence feeds.
- Add production SIEM, metrics, health probes, and disaster recovery runbooks.
- Complete Flutter biometric + secure enclave key management.
