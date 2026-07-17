<!--
Sync Impact Report
- Version change: placeholder template → 1.0.0
- Modified principles: none; this is the first concrete constitution
- Added sections: Core Principles, Architecture and Data Controls,
  Delivery and Quality Gates, Governance
- Removed sections: none
- Templates requiring updates: ✅ .specify/templates/plan-template.md,
  ✅ .specify/templates/spec-template.md,
  ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: none
-->

# AI-Assisted Algorithmic Trading Research and Paper-Trading Platform Constitution

## Core Principles

### I. Evidence-First Research and Execution

Every research result, experiment, and order decision MUST be traceable to an
approved data snapshot, code version, configuration, feature set, and human
approvals. The repository MUST preserve immutable evidence for data, trials,
risk decisions, and execution outcomes; no undocumented state or hidden workflow
may replace the recorded evidence chain.

### II. Human Authority Over Material Controls

AI assistance MAY support analysis and implementation, but MUST NOT approve its
own outputs, change risk limits, access broker secrets, promote live capital,
or bypass required human approvals. Material control points include hypothesis
approval, risk-rule approval, holdout unseal, candidate activation, and any
change to the product boundary.

### III. Deterministic, Point-in-Time Engineering

All features, backtests, validation windows, and reports MUST be deterministic
for a fixed input snapshot and configuration. Systems MUST use point-in-time
semantics, avoid look-ahead, preserve historical universe integrity, and treat
data corrections as new immutable snapshots rather than in-place edits.

### IV. Risk-First Safety and Security

The platform MUST fail closed for authorization, risk, data approval, and broker
actions. Pre-trade risk checks and kill-switch logic MUST be separate from
strategy code, secrets MUST be stored outside source and logs, and every
non-health request MUST authenticate and enforce least privilege.

### V. Verification-Driven Delivery

Every change MUST be implemented with tests, static analysis, dependency
scanning, and evidence that the change satisfies requirements. Production-loop
work MUST include maker-checker review, reproducible artifacts, and explicit
acceptance criteria before completion.

## Architecture and Data Controls

The system MUST be implemented as a modular monolith with explicit boundaries
between research, data, feature, strategy, portfolio, risk, broker, audit, and
UI concerns. The backend MUST use Python 3.12 with FastAPI and Pydantic; the
dashboard MUST use React and TypeScript; data processing MUST use immutable
Parquet and versioned metadata; and persistence MUST use PostgreSQL plus an
S3-compatible artifact store. All external broker integrations MUST remain
behind an adapter boundary and operate only in paper mode for this
constitution's scope. Any expansion to live capital, new jurisdictions, or new
asset classes MUST require a separate approved specification and review.

## Delivery and Quality Gates

Every feature MUST be scoped to a requirement identifier and tracked through
approved artifacts. Tasks MUST preserve traceability, write tests before
claiming completion, and keep state and evidence current. Release or promotion
gates MUST verify data approval, reproducibility, risk checks, security
controls, and independent review before any candidate can advance. The
repository MUST use CI for linting, type checking, dependency scanning,
container scanning, and test execution on every pull request.

## Governance

This constitution supersedes informal practice for this repository. Amendments
require a spec revision, updated supporting templates, and approval from the
relevant Product Owner, Risk Owner, Compliance Owner, and Security Owner before
implementation. Versioning follows semantic rules: MAJOR for
backward-incompatible governance or principle changes, MINOR for new
principles or materially expanded guidance, and PATCH for clarifications or
non-semantic refinements. Every change request MUST show how it preserves
evidence, safety, and approval controls, and any unresolved exceptions MUST be
recorded as explicit TODOs with an owner and expiration.

**Version**: 1.0.0 | **Ratified**: 2026-07-17 | **Last Amended**: 2026-07-17
