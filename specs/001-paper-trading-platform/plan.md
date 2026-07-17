# Implementation Plan: Governed Research and Paper-Trading Platform

**Branch**: `001-paper-trading-platform` | **Date**: 2026-07-17 | **Spec**: [specs/001-paper-trading-platform/spec.md](./spec.md)

**Input**: Feature specification from `specs/001-paper-trading-platform/spec.md`

## Summary

Implement the governed research and paper-trading platform core workflows
required by the spec: immutable data snapshot ingestion, point-in-time feature
computation, deterministic backtests, experiment registry, approval workflows
(maker/checker/risk), paper-candidate activation gates, and broker adapter
integration for Alpaca paper trading. Deliver Phase 0 research artifacts and
Phase 1 design artifacts to enable task creation and implementation planning.

## Technical Context

**Language/Version**: Python 3.12 for backend and research; TypeScript 5 for the dashboard front-end.

**Primary Dependencies**: FastAPI, Pydantic v2, Uvicorn, SQLAlchemy 2, Alembic, Polars, PyArrow, NumPy; testing: pytest, Hypothesis, Playwright for UI contracts; quality: ruff, mypy, bandit, pip-audit.

**Storage**: PostgreSQL 16 for metadata and approvals; S3-compatible object store (MinIO locally) for immutable Parquet artifacts and manifests.

**Testing**: Unit tests with pytest, contract tests for broker/data adapters, integration tests for reconciliation and evidence generation, and end-to-end validation scenarios executed in Docker Compose CI.

**Target Platform**: Linux containers (x86_64 and arm64 compatible) for local development and CI; Docker Compose for orchestration.

**Project Type**: Web-application monorepo with a root-level Python backend and a React/TypeScript frontend under `frontend/`.

**Performance Goals**: Meet repository NFRs: ten-year daily backtest over ~3,000 symbols within ~10 minutes on an 8-core 32 GB reference machine; 15-min bar backtests per spec; pre-trade risk evaluation p95 < 50 ms (excluding external broker calls).

**Constraints**: No live-capital routing; long-only, unlevered posture; trial budget and validation windows per spec; immutable snapshot policy and seven-year retention for raw snapshots unless licensing dictates otherwise.

**Scale/Scope**: Support tens of thousands of experiment records and millions of audit events without changing logical architecture; initial scope is a single-research-team deployment and a single Alpaca paper adapter.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Every task MUST map to one or more approved requirements and preserve
  traceability to the constitution's evidence-first principles. PASS — the
  `spec.md` and this plan preserve traceability requirements.
- The plan MUST preserve point-in-time data handling, immutable artifacts,
  and deterministic validation constraints. PASS — design decisions enforce
  immutable Parquet snapshots and point-in-time feature semantics.
- The design MUST avoid live-capital, unrestricted broker access, and any
  change to risk or compliance boundaries without explicit approval. PASS — no
  live-capital adapters are proposed; broker adapter limited to Alpaca paper
  mode.
- The implementation MUST include tests, static analysis, dependency scanning,
  and evidence for any security, data, or risk-sensitive change. PASS — CI
  gates are required in the plan.

## Glossary

- `ValidationRun` (Trial): deterministic backtest or validation execution.
- `PaperCandidate` (Candidate): frozen candidate derived from a ValidationRun.
- `PaperSession`: recorded paper-trading session used to count toward live-proposal eligibility.

## Project Structure

### Documentation (this feature)

```text
specs/001-paper-trading-platform/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── api/
├── models/
├── services/
├── adapters/
│   └── broker/
├── backtest/
├── features/
├── storage/
├── worker/
└── secrets/

tests/
├── unit/
├── integration/
├── contract/
└── security/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

migrations/
benchmarks/
scripts/
docs/
```

**Structure Decision**: Web-application monorepo with a root-level Python backend under `src/` and a React/TypeScript frontend under `frontend/`.

## Complexity Tracking

None
