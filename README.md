# SentinelKE

SentinelKE is a compliance-first national security and intelligence coordination platform for authorized agencies. This repository now includes V2 advanced intelligence expansion modules with warrant-gated AI workflows, federated collaboration, and forensic automation.

## Included Components
- Django + DRF backend with modular security domain apps
- Django template dashboard (Bootstrap 5, no JS frameworks)
- Lawful forensics and intercept integration adapters (API-based)
- USSD intake endpoint for Africa's Talking
- Flutter field kit with live ops, AI alert, and workspace screens
- Dockerized deployment with PostGIS, Neo4j, Redis, Celery, Gunicorn/Uvicorn, and Nginx
- Python ML microservice stubs (summarization, synthetic media checks, transcription/translation)

## V2 Modules
- `apps/ai_intelligence`: pattern-of-life, predictive scoring, summarization records, synthetic media scans
- `apps/operations`: live command feed, AR overlay packets, translation/transcription records, joint workspaces
- `apps/forensics_advanced`: crypto tracing records, IoT artifacts, cloud legal holds
- `apps/biometrics`: multi-modal fusion queries, behavioral biometrics
- `apps/evidence_automation`: integrity anchoring, automated reports, witness redaction jobs
- `apps/field_ops`: drone feed metadata and offline sync integrity logs
- `apps/federation`: federated query gateway and international exchange logs
- `apps/ai_gateway`: hybrid AI orchestration (Claude, OpenRouter, llama.cpp), sensitivity filtering, caching, and AI request logging

## Compliance Enforcement
- Sensitive V2 endpoints require an active warrant tied to the case.
- Scope/proportionality validation blocks operations that exceed warrant authorization.
- Object-level RBAC enforces agency scope, assignment, and case clearance thresholds.
- Audit records remain cryptographically signed.

## Quick Start (Docker)
1. Copy `backend/.env.example` to `.env` and set production secrets.
2. Start stack:
   - `cd deployment`
   - `docker compose up --build`
3. Apply migrations:
   - `docker compose exec web python manage.py migrate`
4. Create superuser:
   - `docker compose exec web python manage.py createsuperuser`

## Temporary Local Fallback (No Docker)
1. Install dependencies:
   - `python -m pip install -r backend/requirements.txt`
   - `python -m pip install -r ml_services/requirements.txt`
2. Apply local migrations (SQLite profile):
   - `python backend/manage.py migrate --settings=sentinelke.settings_local --noinput`
3. Start local services:
   - `powershell -ExecutionPolicy Bypass -File .\scripts\start_local_stack.ps1`
4. Check health:
   - `powershell -ExecutionPolicy Bypass -File .\scripts\check_local_stack.ps1`
5. Stop services:
   - `powershell -ExecutionPolicy Bypass -File .\scripts\stop_local_stack.ps1`

## Testing
- `python backend/manage.py test apps.core.tests apps.compliance.tests --settings=sentinelke.settings_test`

## WebSocket
- Live operations stream endpoint: `/ws/operations/live/`

## API Surface (high level)
- `/api/core/`
- `/api/compliance/`
- `/api/forensics/`
- `/api/intelligence/`
- `/api/fraud/`
- `/api/geo/`
- `/api/surveillance/`
- `/api/collaboration/`
- `/api/integrations/`
- `/api/ai-intelligence/`
- `/api/operations/`
- `/api/forensics-advanced/`
- `/api/biometrics/`
- `/api/evidence-automation/`
- `/api/field-ops/`
- `/api/federation/`
- `/api/ai/`

## Mobile and Desktop Client Testing
1. Install Flutter SDK and add lutter to PATH.
2. From lutter_field_kit initialize platforms if not present:
   - lutter create .
3. Run tests:
   - lutter test

## Desktop App Mode (Flutter)
- Start desktop client:
  - un_desktop.bat
- This launches Flutter Windows target (native desktop), not a web UI.

## Mobile App Mode (Flutter)
- Start mobile client:
  - un_mobile.bat
- Uses Android target by default (lutter run -d android).
