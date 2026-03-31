# SentinelKE Architecture

## Stack
- Backend: Django + DRF (modular apps)
- Data: PostgreSQL + PostGIS, Neo4j integration hooks
- Frontend: Django templates + Bootstrap 5 + minimal vanilla JS
- Mobile: Flutter field kit
- Integrations: Africa's Talking USSD, lawful forensic/intercept adapters

## Backend Modules
- `core`: agencies, user profiles, case management, RBAC/clearance enforcement primitives
- `compliance`: warrants, approvals, retention policies
- `audit`: cryptographically signed audit events
- `forensics`: seized devices, chain-of-custody, ingestion records
- `intelligence`: source reports, threat signals, graph entities/relations
- `fraud`: financial transactions and anomaly alerts
- `geo`: incident mapping, geofences, geospatial alerts
- `surveillance`: warrant-gated surveillance request workflows
- `collaboration`: notes, secure message envelopes, evidence sharing
- `integrations`: lawful API ingestion and USSD webhook endpoints

## Compliance Controls
- Object-level RBAC enforces agency scope, assignment, and case clearance thresholds.
- Surveillance requests are blocked unless linked warrant is active.
- Every create operation is audit-logged with hash + HMAC signature.
- Retention policies are explicitly modeled for minimization workflows.
- Audit dashboard endpoints are read-only and admin-restricted.

## Threat Model Baseline
- TLS termination at Nginx edge.
- Session + token auth for API access.
- Secure cookie and HSTS defaults enabled.
- Key material designed for HSM-backed replacement.

## Non-Goals
- No exploit delivery systems.
- No jailbreak tooling.
- No password-cracking engines.
- Integrations only with certified lawful systems.

## V2 Expansion
- AI intelligence app adds pattern-of-life baselining, predictive risk scoring, NLP summary records, and synthetic media scan records.
- Operations app adds live asset positions, AR overlay APIs, multilingual transcript storage, and joint task workspaces with WebSocket fan-out.
- Forensics advanced adds crypto transaction intelligence, IoT forensic ingestion, and cloud legal hold orchestration.
- Biometrics app adds multi-modal identity fusion (warrant-gated) and behavioral biometric profiles.
- Evidence automation adds private-ledger hash anchoring, court-report artifacts, and redaction job control plane.
- Field ops adds drone feed metadata and offline sync integrity logs with cryptographic signatures.
- Federation app adds federated search orchestration and international exchange audit trails.

- AI Gateway app introduces hybrid provider routing (Claude/OpenRouter/llama.cpp), compliance-aware prompt sanitization, AI cache, token accounting, and immutable AI request logs.
