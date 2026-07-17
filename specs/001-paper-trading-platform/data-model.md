# data-model.md

**Feature**: Governed Research and Paper-Trading Platform
**Date**: 2026-07-17

## Entities

### Hypothesis
- id: UUID (PK)
- title: string
- rationale: text
- family: enum (trend, mean_reversion, cross_sectional, volatility, ml_ranking)
- created_by: user id
- created_at: timestamp
- status: enum (draft, planned, running, completed, rejected)
- related_trials: list of Trial IDs

### DataSnapshot
- id: content-addressed id (SHA-256)
- provider: string
- license: string
- ingestion_time: timestamp
- range_start: date
- range_end: date
- manifest_path: string
- row_count: integer
- checksum: string
- approval: object {approver, approved_at, rationale}

### ValidationRun (Trial)
- id: UUID
- hypothesis_id: UUID
- snapshot_id: DataSnapshot.id
- code_commit: git sha
- feature_versions: map
- params: JSON
- start_time, end_time
- status: enum (queued, running, failed, completed)
- metrics: JSON
- artifacts: list of artifact refs

### RiskConfiguration
- id: UUID
- name: string
- parameters: JSON (exposure caps, concentration limits, price/liquidity limits)
- created_by, created_at
- approved_by, approved_at

### PaperCandidate
- id: UUID
- hypothesis_id
- validation_run_id
- risk_configuration_id
- created_at
- status: enum (frozen, active, paused, retired)
- approvals: list of ApprovalRecord ids

### ApprovalRecord
- id: UUID
- actor_id
- role: enum (quant_lead, risk_owner, checker, product_owner)
- object_type: enum (snapshot, run, risk_config, candidate)
- object_id: UUID or string
- decision: enum (approved, rejected)
- rationale: text
- timestamp

### Incident
- id: UUID
- type: enum (data_quality, reconciliation, slippage, risk_breach, security)
- severity: enum (low, medium, high, critical)
- created_at, resolved_at
- description, evidence_refs

### PaperSession
- id: UUID
- candidate_id: UUID (PaperCandidate.id)
- session_date: date
- orders_submitted: integer
- fills: integer
- realized_pnl: decimal
- reconciliation_status: enum (pending, reconciled, failed)
- artifacts: list of artifact refs (ledgers, logs)

### PaperOrder
- id: UUID
- paper_session_id: UUID (PaperSession.id)
- candidate_id: UUID
- data_snapshot_id: content-addressed id
- source_decision_id: UUID (reference to decision/event that produced the order)
- risk_check_result_id: UUID
- correlation_id: string
- client_order_id: string
- broker_order_id: string (nullable)
- instrument_id: string (or symbol)
- side: enum (buy, sell)
- order_type: enum (market, limit, stop, stop_limit)
- quantity: decimal
- limit_price: decimal (nullable)
- stop_price: decimal (nullable)
- time_in_force: enum (GTC, IOC, FOK, DAY)
- status: enum (generated, submitted, acknowledged, partially_filled, filled, cancelled, failed)
- submitted_at: timestamp (nullable)
- acknowledged_at: timestamp (nullable)
- terminal_at: timestamp (nullable)
- reject_reason: string (nullable)
- broker_payload_artifact_id: content-addressed id (immutable payload evidence)
- created_at: timestamp
- updated_at: timestamp

Notes:
- All monetary and quantity fields MUST use decimal representations.
- All timestamps MUST use UTC.
- Provider-specific fields (execution_venue, order_flags) may be nullable.
- Preserve original broker payloads as immutable artifacts and record their hashes.
- Enforce unique broker identifiers where supplied.
- `PaperOrder` status transitions MUST follow an explicit state machine.

### PaperFill
- id: UUID
- paper_order_id: UUID (PaperOrder.id)
- paper_session_id: UUID (PaperSession.id)
- candidate_id: UUID
- broker_fill_id: string
- instrument_id: string (or symbol)
- quantity: decimal
- price: decimal
- executed_at: timestamp
- commission: decimal (nullable)
- fees: decimal (nullable)
- currency: string
- execution_venue: string (nullable)
- liquidity_flag: string (nullable)
- broker_payload_artifact_id: content-addressed id (immutable payload evidence)
- created_at: timestamp

Notes:
- `PaperFill` records are append-only and persisted as immutable evidence.
- All monetary and quantity fields MUST use decimal representations.
- All timestamps MUST use UTC.

### LiveProposal
- id: UUID
- candidate_id: UUID
- created_by: user id
- created_at: timestamp
- required_session_count: integer
- status: enum (draft, submitted, approved, rejected)
- evidence_refs: list of artifact refs

## Relationships

- A `Hypothesis` may have many `ValidationRun` entries.
- A `ValidationRun` references one `DataSnapshot` and one or more feature
  versions.
- A `PaperCandidate` is derived from a `ValidationRun` and references a
  `RiskConfiguration` and `ApprovalRecord` items.
- `ApprovalRecord` links actors to approved objects; approvals are required for
  DataSnapshot, RiskConfiguration, and PaperCandidate activation.

## Validation Rules

- Every `ValidationRun` must reference an approved `DataSnapshot` before being
  marked `completed` for publication.
- `DataSnapshot` approval requires the Data Owner role and recorded rationale.
- `PaperCandidate` activation requires Quant Lead and Risk Owner approvals and
  a recorded `DataSnapshot` reference. Checker approval must be recorded as an
  `ApprovalRecord` with `role=checker` and `decision=approved` prior to the
  first activation. Notification or assignment is insufficient.

- Every `PaperOrder` must reference a `PaperSession`, `PaperCandidate`, and
  the `DataSnapshot` used for the session's execution context.
- `PaperFill` records must reference the originating `PaperOrder` and be
  persisted as tamper-evident artifacts to support reconciliation.
