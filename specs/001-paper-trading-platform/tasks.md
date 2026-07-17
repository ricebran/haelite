---
description: "Task list for Governed Research and Paper-Trading Platform"
---

# Tasks: Governed Research and Paper-Trading Platform

**Input**: `spec.md`, `plan.md`, `data-model.md`, `contracts/`, `quickstart.md`

## Phase 1: Setup (Project initialization)
- [x] T001 Initialize Python project, virtual env, and CI config (GitHub Actions) — create `pyproject.toml`, `requirements.txt`, and CI workflow files. (paths: `pyproject.toml`, `.github/workflows/ci.yml`)
- [x] T002 [P] Add linting, formatting, and type-check configs (`ruff`, `mypy`, `pre-commit`) — files: `pyproject.toml`, `.pre-commit-config.yaml`.
- [x] T003 [P] Create Docker Compose local stack (Postgres, MinIO, app) — file: `docker-compose.yml`.
- [x] T004 [P] Add repository `README.md` quickstart instructions referencing `specs/001-paper-trading-platform/quickstart.md`.
- [x] T005 [P] Seed local single-user auth for development (seed script and sample env) — files: `scripts/seed-dev-identity.sh`, `.env.example`.

## Phase 2: Foundational (Blocking prerequisites)
- [ ] T006 Initialize database migrations and base schema (Alembic) — files: `migrations/`, `src/models/__init__.py`.
- [ ] T007 [P] Implement core metadata models and tables: `Hypothesis`, `DataSnapshot`, `ValidationRun`, `RiskConfiguration`, `PaperCandidate`, `ApprovalRecord`, `Incident` — files: `src/models/*.py`.
- [ ] T008 Implement audit service and append-only event model (write-only events table + API hook) — files: `src/services/audit.py`, `src/models/event.py`.
- [ ] T009 Implement artifact storage interface and local MinIO adapter — files: `src/storage/*`, `docker-compose.yml` updates.
- [ ] T010 [P] Implement job queue worker skeleton and idempotent job runner (DB-backed) — files: `src/worker/*`, `src/tasks/*`.
- [ ] T011 Implement initial API skeleton with authentication and RBAC middleware — files: `src/api/app.py`, `src/api/middleware/auth.py`.
- [ ] T012 Implement ApprovalRecord domain service and persistence (`POST /approvals`) — responsibilities:
- data model and persistence for `ApprovalRecord`
- `POST /approvals` API
- role and decision validation and anti-self-approval rules
- immutable audit event creation and idempotency handling
- domain and API tests
	 Files: `src/api/approvals.py`, `src/services/approval.py`, `src/models/approvals.py`, `tests/unit/test_approvals.py`.
- [ ] T013 Implement DataSnapshot registration and approval endpoints (`POST /data-snapshots`, `/data-snapshots/{id}/approve`) — files: `src/api/snapshots.py`.
- [ ] T014 Implement Hypothesis CRUD endpoints (`POST /hypotheses`, `GET /hypotheses/{id}`) — files: `src/api/hypotheses.py`.
- [ ] T015 Implement ValidationRun creation and finalization endpoints (`POST /runs`, `/runs/{id}/finalize`) and trial registry persistence — files: `src/api/runs.py`, `src/services/runs.py`.
- [ ] T016 [P] Create basic feature computation runner interface (point-in-time semantics) — files: `src/features/*`.
- [ ] T017 Implement backtest engine skeleton and deterministic runner (accepts snapshot, commit, params) — files: `src/backtest/*`.
- [ ] T018 Implement RiskConfiguration CRUD and approval endpoints (`POST /risk-configs`, `/risk-configs/{id}/approve`) — files: `src/api/risk.py`.
- [ ] T019 Implement PaperCandidate creation endpoint (`POST /candidates`) to create a `PaperCandidate` from a `ValidationRun` (creation only; no activation guard) — files: `src/api/candidates.py`, `src/services/candidates.py`.
- [ ] T020 [P] Implement evidence bundle exporter (`GET /evidence/{run_or_candidate_id}`) producing manifest, ledgers, approvals — files: `src/services/evidence.py`.
- [ ] T021 Add test harness and initial unit test examples (pytest) — files: `tests/unit/test_sample.py`.

## Phase 3: User Story 1 - Research a trading idea and prepare evidence (P1)
- [ ] T022 [US1] Create UI/API flow for creating a `Hypothesis` and linking an approved `DataSnapshot` — files: `src/api/hypotheses.py`, `frontend/src/pages/hypotheses/*`.
- [ ] T023 [US1] Implement run submission that creates a `ValidationRun` and enqueues the deterministic backtest job — files: `src/api/runs.py`, `src/worker/jobs/backtest_job.py`.
- [ ] T024 [US1] Persist run artifacts to artifact store with checksums and manifest references — files: `src/services/artifacts.py`.
- [ ] T025 [US1] Implement run finalization that validates snapshot approval and records metrics/artifacts — files: `src/api/runs.py`.
- [ ] T026 [US1] Add contract tests for run lifecycle (create → complete → evidence export) — files: `tests/contract/test_runs.py`.

## Phase 4: User Story 2 - Approve risk controls and activate a paper candidate (P1)
- [ ] T027 [US2] Implement UI/API to author `RiskConfiguration` objects and persist versioned parameters — files: `src/api/risk.py`, `frontend/src/pages/risk/*`.
- [ ] T028 [US2] Implement approval workflow orchestration — responsibilities:
- approval queues and assignments
- pending-approval queries and workflow status/history views
- notifications and frontend workflow integration where applicable
- must call the T012 ApprovalRecord service and MUST NOT persist `ApprovalRecord` directly or duplicate `POST /approvals`
- dependent on: T012
	 Files: `src/services/approval_workflow.py`, `src/api/approval_workflow.py`, `frontend/src/pages/approvals/*`, `tests/integration/test_approval_workflow.py`.
- [ ] T029 [US2] Ensure candidate creation associates existing `ApprovalRecord` references (link approvals to `PaperCandidate.approvals`) and populate approvals list on creation — files: `src/api/candidates.py`.
- [ ] T030 [US2] Implement activation endpoint `POST /candidates/{id}/activate` that enforces readiness criteria (requires Quant Lead + Risk Owner approvals and an explicit `ApprovalRecord` with `role=checker` and `decision=approved` prior to first activation). Add server-side rejection when Checker approval is absent. — files: `src/api/candidates.py`, `src/services/candidates.py`.
	Dependencies: T012 (approval records must exist), T029 (candidate creation)
- [ ] T031 [US2] Add integration tests validating activation guard rejects incomplete approvals and specifically rejects activation when Checker approval record is missing or decision != approved — files: `tests/integration/test_candidate_activation.py`.

## Phase 5: User Story 3 - Review evidence and close a production-loop task (P2)
- [ ] T032 [US3] Implement Checker assignment/notification and Checker review endpoints to accept/reject tasks — files: `src/api/checker.py`, `src/services/notifications.py`.
- [ ] T033 [US3] Implement evidence bundle viewer and acceptance action that updates `ValidationRun`/`PaperCandidate` status — files: `frontend/src/pages/evidence/*`, `src/api/evidence.py`.
- [ ] T034 [US3] Add contract tests for Checker acceptance and rejection paths — files: `tests/contract/test_checker.py`.

## Phase 6: Polish & Cross-Cutting Concerns
- [ ] T035 [P] Add CI steps: lint, type-check, unit tests, contract tests, dependency scan — update `.github/workflows/ci.yml`.
- [ ] T036 [P] Add end-to-end quickstart verification script referencing `quickstart.md` — files: `scripts/validate-quickstart.sh`.
- [ ] T037 [P] Update documentation: `docs/architecture.md`, `docs/governance.md` summarizing constitution rules and readiness criteria.
- [ ] T038 [P] Security hardening & secrets workstream: secret scanner config, runtime secrets-provider integration (connector), CI secret-leak tests, runtime/integration tests ensuring no credentials in repository or evidence bundles, and operating documentation — files: `docs/security.md`, `src/secrets/*`, `tests/security/test_no_secrets.py`, `.github/workflows/secret-scan.yml`.
- [ ] T039 [P] Accessibility and UX polish for dashboard pages created — files: `frontend/src/*`.
- [ ] T040 [P] Implement paper-session persistence and session counter service (`src/services/session.py`, `src/api/sessions.py`) to record `PaperSession` and provide session counts per candidate.
- [ ] T041 [P] Implement PaperSession reconciliation scheduler and status persistence: job orchestration, reconciliation-status updates, and summary status aggregation (do NOT implement detailed order/fill comparison logic or the detailed reconciliation report API). Files: `src/services/reconciliation_scheduler.py`, `src/services/session.py`.
- [ ] T042 [US2] Implement live-capital proposal eligibility gate service and API (`src/services/gates.py`, `src/api/proposals.py`) that enforces required session counts before proposals can be created/submitted. Dependencies: T040, T041, T058.
- [ ] T043 [P] Implement runtime pre-trade risk checks invoked prior to order generation (service + integration tests) — files: `src/services/risk_checks.py`, `src/tests/test_risk_checks.py`.
- [ ] T044 [P] Add performance benchmark harness and CI benchmark job to validate reference backtest durations and risk-check latencies — files: `benchmarks/`, `.github/workflows/benchmarks.yml`.
- [ ] T045 [P] Implement metrics endpoint, monitoring dashboard slices, stale-data alerts, and incident visibility (update `src/api/metrics.py`, `src/services/alerts.py`).
- [ ] T046 [P] Secrets verification and integration tests: add verification harness that ensures secrets-provider integration tasks completed (calls T038) and proves secrets are not present in evidence bundles; runtime checks to ensure only paper credentials used — files: `tests/security/test_secrets_integration.py`, `scripts/verify-secrets.sh`. Dependencies: T038.
- [ ] T047 [P] Frontend scaffold: create `frontend/` Vite React starter and baseline pages to satisfy frontend task references (`frontend/package.json`, `frontend/src/`).
- [ ] T048 [P] Add operational readiness evidence tasks: create `scripts/verify-licensed-data.sh` and `scripts/verify-broker-credentials.sh` and API hooks to record evidence artifacts for licensed data and broker credential provisioning.
- [ ] T049 [P] Implement paper-only broker adapter (Alpaca paper-mode) and adapter contract tests — files: `src/adapters/broker/alpaca_paper.py`, `tests/contract/test_broker_adapter.py`.
- [ ] T050 [P] Implement `PaperOrder` and `PaperFill` persistence, DB models, migrations, append-only fill handling, and ledger export — files: `src/models/orders.py`, `migrations/`. Dependency: T006 (migrations base).
- [ ] T051 [P] Implement order-generation service that turns strategy signals into persisted `PaperOrder` records and exposes `POST /orders` (no live-capital path) — files: `src/services/order_generation.py`, `src/api/orders.py`. Dependencies: T049, T050.
- [ ] T052 [P] Add adapter and order lifecycle contract tests: generation → submit → persists → fill ingestion — files: `tests/contract/test_orders_lifecycle.py`. Dependencies: T049, T050, T051.
- [ ] T053 [P] Implement reconciliation engine comparing generated orders, submitted paper orders, fills, positions, and evidence artifacts; add detailed reconciliation reporting API — files: `src/services/reconciliation_engine.py`, `src/api/reconciliation_report.py`. Dependencies: T041, T050, T052.
- [ ] T054 [P] Enforce no-live-capital policy using a repository-native Python/pytest policy guard executed in CI. Requirements:
- explicit paper-only execution mode
- startup failure when a live-capital mode or live broker endpoint is configured
- adapter-registry test proving only paper adapters are registered
- configuration tests rejecting live-order submission routes
- tests proving paper credentials/endpoints cannot be silently replaced with live equivalents
- CI policy test checking app configuration, adapter registration, and prohibited live execution paths
- fail-closed behavior when broker mode cannot be determined
- Do NOT introduce external policy platforms for initial implementation; use pytest-based guards and runtime checks.
	 Dependencies: T049, T050
- [ ] T055 [P] Implement automatic iteration-stop enforcement (FR-005) and tests for trial budget exhaustion, missing/revoked approvals, data quality gate failures, risk limit breaches, unresolved reconciliation, and critical incidents — files: `src/services/iteration_guard.py`, `tests/integration/test_iteration_stop.py`. Dependencies: T012, T015, T041.
- [ ] T056 [P] Clarify SC-004 enforcement tests: add tests proving only `PaperSession` with `reconciliation_status = reconciled` count toward `LiveProposal` eligibility — files: `tests/integration/test_proposal_eligibility.py`. Dependencies: T040, T041, T042, T058.
- [ ] T057 [P] Implement operational-status API `GET /status/operational` and contract tests summarizing health, incidents, data freshness, reconciliation status, and evidence availability — files: `src/api/status.py`, `tests/contract/test_operational_status.py`. Dependencies: T045, T041, T020.
- [ ] T058 [P] Implement `LiveProposal` persistence and migrations; add model, migration, and persistence tests — files: `src/models/live_proposals.py`, `migrations/`, `tests/unit/test_live_proposals.py`. Dependencies: T006.

## Dependencies & Execution Order
- Setup (Phase 1) → Foundational (Phase 2) must complete before user stories.
- User Stories (Phase 3-5) may proceed in parallel after Phase 2, subject to dependencies.

## Parallel Opportunities
- Tasks marked `[P]` can be worked on in parallel by multiple engineers.

## Implementation Strategy
- MVP focus: deliver User Story 1 minimal end-to-end (create hypothesis, run validation, produce evidence) first, then add approvals and candidate activation (User Story 2), then Checker flows and polish.


## Summary
- Total tasks: 58
- Phase 1 tasks: 5
- Phase 2 tasks: 16
- Phase 3 tasks: 5
- Phase 4 tasks: 5
- Phase 5 tasks: 3
- Phase 6 tasks: 24
- US1 tasks: 5
- US2 tasks: 6
- P1 story tasks (US1 + US2): 11
- US3 / P2 story tasks: 3


**Next step**: run `/speckit-implement` or convert tasks to issues with `/speckit-taskstoissues`.
