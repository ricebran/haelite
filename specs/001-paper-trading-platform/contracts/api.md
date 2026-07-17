# API Contracts: Governed Research and Paper-Trading Platform

**Base path**: `/api/v1`

## Authentication
- All non-health endpoints require authentication and role-based authorization.

## Endpoints (summary)

### Hypotheses
- `POST /hypotheses` — create hypothesis (body: title, rationale, family)
- `GET /hypotheses/{id}` — retrieve hypothesis
- `GET /hypotheses` — list hypotheses with filters

### Data Snapshots
- `POST /data-snapshots` — register a new snapshot manifest (body: manifest path, checksum, provider, range)
- `GET /data-snapshots/{id}` — retrieve snapshot metadata and approval status
- `POST /data-snapshots/{id}/approve` — record approval (role restricted to Data Owner)

### Validation Runs (Trials)
- `POST /runs` — create a validation run (body: hypothesis_id, snapshot_id, params)
- `GET /runs/{id}` — run status and artifacts
- `POST /runs/{id}/finalize` — mark run complete (requires snapshot approved)

### Risk Configurations
- `POST /risk-configs` — create risk configuration (body: parameters)
- `POST /risk-configs/{id}/approve` — record approval (role restricted to Risk Owner)

### Paper Candidates
- `POST /candidates` — create a paper candidate from a run (body: run_id, risk_config_id)
- `POST /candidates/{id}/activate` — activate candidate for paper trading (requires Quant Lead + Risk Owner + Checker approvals recorded)
 - `POST /candidates/{id}/activate` — activate candidate for paper trading (requires Quant Lead + Risk Owner approvals and an explicit Checker approval `ApprovalRecord` with `role=checker` and `decision=approved` recorded prior to activation). Implementations MUST reject activation requests when a Checker approval is absent.
- `GET /candidates/{id}` — retrieve candidate status and approvals

### Paper Sessions
- `POST /sessions` — record a paper session after a paper trading day (body: candidate_id, session_date, orders_submitted, fills, realized_pnl)
- `GET /sessions/{id}` — retrieve session details and reconciliation status
- `GET /sessions?candidate_id={id}` — list sessions for a candidate

### Orders & Fills
- `POST /orders` — create/persist a generated paper order (body: candidate_id, session_id, snapshot_id, side, quantity, price, metadata)
- `GET /orders/{id}` — retrieve persisted paper order
- `POST /fills` — record a fill for a persisted order (body: order_id, quantity, price, broker_fill_id, settlement_info)
- `GET /fills/{id}` — retrieve fill details

### Operational Status
- `GET /status/operational` — aggregate system health, active incidents, data freshness, reconciliation status, and evidence availability (role-limited). Use for dashboards and readiness checks.

### Live Proposals
- `POST /proposals` — create a live-capital proposal for a candidate (body: candidate_id, evidence_refs)
- `GET /proposals/{id}` — retrieve proposal status

Notes:
- `POST /proposals` MUST validate that the candidate has at least 60 completed
	`PaperSession` records with `reconciliation_status = reconciled` before
	allowing proposal creation/submission; proposal creation is an eligibility
	step and does not perform any live-capital activation. Failed or
	unreconciled sessions do not count.

- Implementations MUST NOT expose any live-capital order submission endpoints
	or introduce any live-capital execution paths. Broker adapters are strictly
	paper-only in scope for this feature.

### Metrics & Monitoring
- `GET /metrics` — operational metrics endpoint (role-limited)

### Approvals and Evidence
- `POST /approvals` — record an approval (actor, role, object_type, object_id, decision, rationale)
- `GET /evidence/{run_or_candidate_id}` — download evidence bundle (manifests, checksums, ledgers)

### Admin / Operational
- `GET /health` — health endpoint (no auth)
- `GET /metrics` — operational metrics (role-limited)

## Contract Notes
- All write operations create audit events that are append-only and tamper-evident.
- Approval endpoints enforce role-based authorization and require an explicit rationale.
- Implementations MUST validate that snapshots are approved before allowing finalization or candidate activation.
