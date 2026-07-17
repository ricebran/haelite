# Feature Specification: Governed Research and Paper-Trading Platform

**Feature Branch**: `001-paper-trading-platform`

**Created**: 2026-07-17

**Status**: Draft

**Input**: User description: "Use haelite.md as the authoritative project brief. Produce a complete, testable specification and identify genuine ambiguities without inventing requirements."

## Scope, Safety, and Governance Constraints *(mandatory)*

- The feature MUST remain within the approved product boundary for internal
  research and paper trading only.
- The feature MUST preserve human approval gates for material controls,
  including risk, data, and release decisions.
- The feature MUST not introduce live-capital routing, client-asset handling,
  advisory output, or unapproved changes to risk limits.
- The feature MUST maintain traceability to approved data snapshots,
  configurations, approvals, and evidence artifacts.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Research a trading idea and prepare evidence (Priority: P1)

A research team member needs to develop a hypothesis, run validation work, and
record evidence so the idea can be reviewed and approved without losing
traceability.

**Why this priority**: This is the core value of the platform and establishes
that every result can be defended and audited.

**Independent Test**: A user can create a hypothesis, attach the approved data
snapshot and validation context, and produce a review-ready evidence record.

**Acceptance Scenarios**:

1. **Given** a new hypothesis and an approved research window, **When** the
   researcher records the hypothesis and related context, **Then** the system
   stores a traceable record with the relevant data snapshot, configuration,
   and status.
2. **Given** a completed validation run, **When** the researcher finalizes the
   results, **Then** the system preserves the evidence and prevents the run from
   being treated as complete without required metadata.

---

### User Story 2 - Approve risk controls and activate a paper candidate (Priority: P1)

A Risk Owner and the relevant approvers need to review the proposed risk
configuration and candidate readiness before the system can generate paper
orders.

**Why this priority**: Risk controls are central safety gates and must remain
separate from strategy logic.

**Independent Test**: An authorized approver can review a candidate, approve the
risk configuration, and activate the candidate for paper-trading use only.

**Acceptance Scenarios**:

1. **Given** a candidate that meets the readiness criteria, **When** the
   required approvals are recorded, **Then** the system allows the candidate to
   proceed to paper-trading activation.
2. **Given** a request to change active risk limits, **When** the change is
   submitted, **Then** the system rejects it unless the required approval flow
   is completed.

#### Paper Candidate Readiness Criteria

For the initial MVP, a strategy candidate is considered READY for paper-trading
activation when all of the following minimal conditions are met:

- Quant Lead approval for the hypothesis and candidate configuration is
  recorded.
- Risk Owner approval for the candidate's risk configuration is recorded.
- The candidate references an approved `Data Snapshot` (immutable dataset
  manifest and checksum) used for validation and reporting.
- A Checker approval for the candidate is recorded prior to first activation.

These minimal readiness criteria prioritize governance and traceability while
allowing timely activation. Notification alone is NOT sufficient — explicit
Checker approval is required before the first paper-trading activation. Any
future relaxation or tightening of these gates MUST be recorded as a spec-level
change.

---

### User Story 3 - Review evidence and close a production-loop task (Priority: P2)

A Checker needs to verify traceability, approvals, and outcome evidence before
marking a task or phase complete.

**Why this priority**: Independent review is required to maintain governance and
prevent self-approval.

**Independent Test**: A Checker can inspect the evidence bundle for a task and
accept or reject completion with an auditable decision.

**Acceptance Scenarios**:

1. **Given** a completed research or paper-trading task, **When** the Checker
   reviews the evidence and related approvals, **Then** the system records an
   acceptance or rejection decision tied to the task.
2. **Given** a task that lacks required evidence or approvals, **When** the
   Checker reviews it, **Then** the system blocks completion and identifies the
   missing controls.

---

### Edge Cases

-- What happens when the required data snapshot, licensed-data evidence, or
  approval record is missing before a trial or order generation run?
- How does the system handle repeated failure patterns or exhausted trial
  budgets?
- What happens when market data goes stale or a risk breach occurs during paper
  trading?
- How does the system behave if an attempt is made to convert paper settings to
  live-capital behavior?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST treat the approved specification as the source of
  truth and preserve traceable links from every research task, experiment,
  report, and approval to the relevant requirement and governance context.
- **FR-002**: The system MUST maintain distinct roles for research, risk,
  compliance, security, operations, and independent review, and MUST prevent
  self-approval for final completion decisions.
- **FR-003**: The system MUST record approvals for data snapshots, experiment
  plans, risk rules, holdout access, and candidate activation with the actor,
  decision, timestamp, object, and rationale.
- **FR-004**: The system MUST maintain a current state record for each research
  program, including phase, completed tasks, active blockers, trial counts,
  holdout status, and the next approved task.
- **FR-005**: The system MUST stop iteration when acceptance criteria are met,
  the trial budget is exhausted, the same failure repeats, required information
  is missing, or a required approval has not been recorded.
- **FR-006**: The system MUST enforce the approved product boundaries by
  excluding live-capital routing, client-asset management, customer-facing
  advisory output, and other out-of-scope activities from the supported workflow.
- **FR-007**: The system MUST preserve immutable evidence for data, experiments,
  risk decisions, approvals, and execution outcomes so that every reported result
  can be audited.
- **FR-008**: The system MUST support immutable historical market-data ingestion,
  point-in-time feature calculation, and deterministic validation across the
  specified in-sample, walk-forward, and holdout windows.
- **FR-009**: The system MUST enforce the approved portfolio, exposure, and
  order limits, including long-only posture, position caps, price and liquidity
  eligibility, and kill-switch behavior.
- **FR-010**: The system MUST support paper-trading order generation,
  reconciliation, and incident handling without allowing automatic promotion to
  live capital.
- **FR-011**: The system MUST expose operational status, active incidents, risk
  conditions, and evidence availability in a way that supports oversight and
  review.
- **FR-012**: The system MUST protect sensitive credentials and authentication
  material by preventing direct exposure in source, workflows, logs, or
  evidence artifacts.

### Key Entities *(include if feature involves data)*

- **Hypothesis**: A research idea with its economic rationale, validation plan,
  budget context, and current status.
- **Data Snapshot**: An immutable approved dataset version that defines the
  historical window, integrity checks, and lineage for a run.
- **Validation Run**: A recorded in-sample, walk-forward, or holdout exercise
  that includes results, windows, configuration, and evidence references.
- **Risk Configuration**: The approved rules that govern exposure, kill-switch
  behavior, and order eligibility.
- **Paper Candidate**: A frozen strategy candidate that is eligible for paper
  trading only after the required approvals and checks pass.
- **Approval Record**: A signed decision that records who approved a change,
  what object was approved, and why.
- **Incident**: A recorded operational or risk event that affects execution,
  monitoring, or evidence quality.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of reported results and paper-trading decisions are traceable
  to an approved data snapshot, configuration, and recorded approval.
- **SC-002**: 100% of material phase transitions require the required approvals
  before the system allows progression to the next stage.
- **SC-003**: The platform supports one complete research-to-validation-to-paper
  candidate workflow within the documented study windows and trial budget.
- **SC-004**: The system supports at least 60 completed `PaperSession` records
  with `reconciliation_status = reconciled` before a LiveProposal may be
  created or submitted. Failed, cancelled, partial, unreconciled, or disputed
  sessions do NOT count toward this threshold.
- **SC-005**: No live-capital orders, client-asset flows, or unapproved risk
  changes occur in the supported workflow.

## Assumptions

- The initial release targets an internal research team operating in the United
  States with the documented roles and approval structure.
- The default baseline for the first release uses the approved historical windows,
  trial budget, portfolio limits, and paper-trading posture defined in the brief.
- The initial release assumes a single paper-trading environment and a single
  broker adapter path, with any expansion treated as a separate approved change.
- The exact onboarding workflow for market-data licensing and broker access is
  treated as an operational prerequisite rather than a product requirement in
  this specification.

## Glossary (terminology normalization)

- `Hypothesis`: A research idea with economic rationale, validation plan, and status.
- `DataSnapshot`: An immutable approved dataset version that defines the historical window, integrity checks, and lineage for a run.
- `ValidationRun`: A deterministic execution of a backtest or validation fold tied to a `DataSnapshot`, code commit, and parameters. Use `Trial` only as an explanatory alias in this glossary.
- `RiskConfiguration`: The approved rules that govern exposure, kill-switch behavior, and order eligibility.
- `PaperCandidate`: A frozen strategy candidate derived from a completed `ValidationRun` and associated risk configuration and approvals.
- `ApprovalRecord`: Immutable record of an approval decision with actor_id, role, object_type, object_id, decision, rationale, and timestamp.
- `Incident`: A recorded operational or risk event affecting execution, monitoring, or evidence quality.
- `PaperSession`: A recorded paper-trading session (one market day of paper trading activity) used to satisfy live-proposal eligibility counts.
- `PaperOrder`: A persisted paper order generated by the order-generation service; includes candidate_id, session_id, snapshot_id, timestamp, quantity, price, side, status, and broker_order_id.
- `PaperFill`: A persisted fill/execution record linked to a `PaperOrder` and `PaperSession`, including fill price, quantity, timestamp, broker_fill_id, and settlement metadata.
- `LiveProposal`: A submission representing a request to consider live-capital for a `PaperCandidate` (requires evidence and eligibility gates).

Use these canonical names when referring to persisted entities, APIs, or tasks. Lowercase words such as "session" or "run" may be used for narrative text only when they do not refer to the formal entities above.
