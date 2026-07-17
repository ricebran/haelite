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

- Decision: Initial PaperCandidate activation requires recorded Quant Lead,
  Risk Owner, and explicit Checker approvals, together with an approved
  DataSnapshot reference.
- Rationale: Explicit Checker approval provides independent verification and
  enforces maker-checker separation before activation.
- Rejected alternative: Checker notification or assignment without an approval
  decision.
- Clarification: An N-session requirement is not required before initial paper
  activation; 60 completed, reconciled PaperSession records are required only
  before LiveProposal creation or submission.

## Open Questions (deferred to operations)

- Data licensing onboarding procedures and the operational steps for acquiring
  licensed historical data snapshots (treated as an operational prerequisite).
- Broker credential onboarding and access provisioning steps (treated as an
  operational prerequisite and subject to Security Owner policies).
