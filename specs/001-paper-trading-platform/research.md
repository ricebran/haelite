# research.md

**Feature**: Governed Research and Paper-Trading Platform
**Date**: 2026-07-17

## Decisions

1. Implementation language and stack

- Decision: Use Python 3.12 backend with FastAPI, Pydantic v2, SQLAlchemy 2,
  Polars/PyArrow for data processing, PostgreSQL for metadata, and S3-compatible
  artifact storage. Frontend: React + TypeScript.
- Rationale: Matches project baseline in `haelite.md` and the technology
  baseline already approved for the repository.
- Alternatives considered: Go or Rust for compute-heavy tasks — rejected due to
  team familiarity and existing ecosystem alignment with Python data stack.

2. Candidate readiness gate

- Decision: Adopt minimal approvals readiness for MVP: recorded Quant Lead and
  Risk Owner approvals, an approved Data Snapshot reference, and Checker
  notification/assignment before activation.
- Rationale: Balances governance with the need for timely experimentation and
  aligns with the constitution's human-authority rule. Stricter operational
  gates (dry-run sessions) are deferred to a later spec revision.
- Alternatives considered: stricter operational requirement (N-session dry-run)
  or automated performance thresholds; deferred to future iteration.

## Open Questions (deferred to operations)

- Data licensing onboarding procedures and the operational steps for acquiring
  licensed historical data snapshots (treated as an operational prerequisite).
- Broker credential onboarding and access provisioning steps (treated as an
  operational prerequisite and subject to Security Owner policies).
