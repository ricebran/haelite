# AI-Assisted Algorithmic Trading Research and Paper-Trading Platform: Master Product Requirements and Implementation Specification

**Version:** 1.0  
**Date:** July 17, 2026  
**Status:** Implementation baseline; repository adoption requires Project Sponsor approval.  
**Mode:** Research and paper trading only.

Live-capital deployment, client assets, and public investment advice are outside this specification.

## 1. Executive Summary

This document converts the supplied AI trading project and research-process material into a complete, internally consistent implementation baseline for Spec Kit.

- Internal AI-assisted research, validation, risk, and paper-trading platform.
- Liquid U.S.-listed common stocks and unleveraged ETFs; USD 100,000 long-only reference portfolio.
- Fixed in-sample, walk-forward, and one-time sealed-holdout discipline.
- Immutable data, features, experiments, approvals, risk decisions, and evidence.
- Alpaca paper trading only; live endpoints prohibited.
- Human approval at all material control points.

## 2. Document Authority and Change Control

After approval and repository commit, this document is the source of truth. Generated artifacts may add detail but may not weaken controls or change numeric limits without a spec-level revision.

## 3. Fixed Baseline Decisions

| Decision | Approved baseline |
| --- | --- |
| Product boundary | Internal proprietary research and paper trading only. The MVP does not provide investment advice, manage client assets, accept deposits, route live-capital orders, or expose broker credentials to autonomous agents. |
| Jurisdiction | United States operating context for an internal research team. Expansion to another jurisdiction or a customer-facing product is a separate spec-level event requiring legal and compliance review. |
| Asset class | U.S.-listed common stocks and unleveraged exchange-traded funds on NYSE, Nasdaq, and NYSE Arca. OTC securities, options, futures, cryptoassets, preferred shares, warrants, leveraged ETFs, and inverse ETFs are excluded. |
| Trading frequency | Daily and 15-minute bar research. The default production candidate calculates signals after the market close and submits paper orders during the next regular session. High-frequency and sub-minute trading are excluded. |
| Reference capital | A USD 100,000 paper portfolio is used for sizing, capacity checks, risk thresholds, and acceptance tests. |
| Portfolio posture | Long-only, unlevered, maximum 20 concurrent positions, no short sales, no derivatives, and no pre-market or after-hours orders. |
| Historical window | Research history begins January 1, 2016 and ends December 31, 2025. Data after December 31, 2025 is reserved for forward paper-trading and future validation revisions. |
| Validation windows | In-sample: 2016-01-01 through 2021-12-31. Walk-forward validation: 2022-01-01 through 2023-12-31. Sealed holdout: 2024-01-01 through 2025-12-31. The holdout is evaluated once after code, parameters, data snapshot, and risk rules are frozen. |
| Trial budget | Maximum 5 strategy families, 10 hypotheses per family, 50 total logged hypothesis trials, 25 parameter-search jobs, 2 paper-trading candidates, and 1 sealed-holdout evaluation for the frozen finalist. |
| Initial broker adapter | Alpaca paper trading is the first external execution adapter. The broker interface remains abstract so additional paper or live adapters require a separate approved feature specification. |
| Historical data interface | The repository implements an immutable LocalParquetProvider and a vendor-neutral HistoricalBarProvider interface. Licensed external data is imported only as versioned Parquet snapshots with manifests and checksums. |
| Implementation architecture | A modular monolith in Python 3.12 with FastAPI, Pydantic, SQLAlchemy, PostgreSQL, Parquet, Polars, and an S3-compatible artifact store. A React and TypeScript dashboard is a thin client over the API. |
| Deployment | Docker Compose for local and paper-trading environments. CI runs on every pull request. Production cloud selection and live-trading infrastructure are out of scope. |
| Human authority | A human Product Owner approves scope; a Quant Lead approves research hypotheses; a Risk Owner approves risk rules; a Compliance Owner approves policy controls; and a Checker independent of the Maker approves production-loop completion. |

## 4. Product Vision, Users, and Positioning

Build a governed platform that lets a small internal quantitative team research, test, validate, approve, monitor, and paper trade algorithmic strategies while preserving a reproducible evidence chain from data snapshot to final decision.

### Primary users

| Role | Responsibility | Decision authority |
| --- | --- | --- |
| Project Sponsor | Owns business intent, funding, and final go/no-go decisions. | Approves repository adoption and any future live-capital program. |
| Product Owner | Owns this PRD, scope, priorities, and acceptance criteria. | Approves feature-level changes that do not alter risk, compliance, or live-capital boundaries. |
| Quant Lead | Owns hypotheses, validation design, trial budget, and strategy review. | Approves experiment plans before runs and confirms holdout freeze readiness. |
| Data Owner | Owns data licensing, manifests, point-in-time integrity, and corporate-action handling. | Approves every data snapshot used for reported metrics. |
| Risk Owner | Owns limits, kill switches, exposure controls, and incident escalation. | Approves risk-rule changes and paper-trading candidate activation. |
| Compliance Owner | Owns policy interpretation, audit retention, and jurisdictional review. | Approves customer-facing, advisory, multi-jurisdiction, or live-trading scope changes. |
| Security Owner | Owns identity, secrets, dependency scanning, and incident response. | Approves broker credential handling and security exceptions. |
| Maker | Implements one traceable task, adds tests, runs narrow checks, and updates STATE.md. | Cannot approve own production-loop completion. |
| Checker | Independently verifies spec traceability, tests, trial counts, data integrity, and unrelated changes. | Accepts or rejects task and phase completion. |

### In scope

- Immutable, versioned market-data ingestion and snapshot manifests.
- Point-in-time feature computation for daily and 15-minute bars.
- Configuration-driven baseline and candidate strategies.
- Deterministic backtesting with transaction costs, slippage, liquidity, and realistic order timing.
- Walk-forward validation, a sealed holdout gate, and immutable experiment logging.
- Portfolio construction, position sizing, pre-trade risk checks, post-trade monitoring, and kill switches.
- Alpaca paper-trading integration behind a broker adapter.
- Human approval gates, audit logs, role-based access, and reproducible reports.
- A minimal dashboard for experiment, risk, portfolio, and operational status.
- CLI and API workflows suitable for Spec Kit-generated plans and tasks.

### Explicit non-goals

- Live-capital order routing or automatic promotion from paper to live.
- Customer accounts, public investment recommendations, advisory services, copy trading, or custody.
- Short selling, margin, options, futures, cryptoassets, swaps, or other derivatives.
- High-frequency, market-making, co-location, or latency-arbitrage strategies.
- Autonomous self-modification of signal, execution, or risk logic.
- Automatic risk-threshold changes, credential rotation by an agent, or unrestricted model tool access.
- Multi-tenant billing, public API monetization, mobile applications, and brokerage operations.
- Repeated tuning against the sealed holdout or unlogged experimental searches.

## 5. Architecture

| Component | Responsibility |
| --- | --- |
| Web dashboard | React + TypeScript client for authenticated research, experiment, risk, portfolio, and incident views. |
| API application | FastAPI service exposing versioned REST endpoints, enforcing authorization and schema validation. |
| Research orchestrator | Runs data builds, feature jobs, backtests, walk-forward jobs, simulations, and reports as traceable tasks. |
| Data subsystem | Imports immutable Parquet snapshots, validates schemas and lineage, and publishes approved datasets. |
| Feature subsystem | Computes point-in-time features with explicit availability timestamps and deterministic transformations. |
| Strategy subsystem | Loads approved strategy definitions and emits target scores or target weights without direct broker access. |
| Portfolio subsystem | Transforms signals into constrained target positions and rebalance orders. |
| Backtest subsystem | Simulates order timing, fills, costs, slippage, corporate actions, and portfolio accounting. |
| Validation subsystem | Runs walk-forward folds, enforces trial budgets, seals holdouts, and aggregates metrics. |
| Risk subsystem | Performs pre-trade, intraday, and end-of-day checks; owns kill-switch state independent of strategy code. |
| Broker adapter | Maps approved orders to Alpaca paper trading and reconciles broker state with internal state. |
| Experiment registry | Stores immutable trial metadata, code version, parameters, data snapshot, windows, metrics, and artifacts. |
| Audit service | Writes append-only security, approval, experiment, data, risk, and execution events. |
| Artifact store | Stores immutable datasets, reports, logs, and model artifacts under content-addressed paths. |
| Metadata database | PostgreSQL stores normalized operational metadata, approvals, configurations, and references to artifacts. |
| Monitoring and alerting | Collects health, latency, data freshness, risk, reconciliation, and error metrics. |

### Technology baseline

| Area | Decision |
| --- | --- |
| Language/runtime | Python 3.12 for backend and research; TypeScript 5 for the dashboard. |
| API | FastAPI, Pydantic v2, Uvicorn. |
| Data processing | Polars, PyArrow, NumPy, pandas only where a dependency requires it. |
| Persistence | PostgreSQL 16 with SQLAlchemy 2 and Alembic migrations. |
| Artifacts | Parquet and JSON in an S3-compatible object store; local MinIO in Docker Compose. |
| Task execution | A database-backed job queue with idempotent workers; no hidden in-process background jobs for critical workflows. |
| Frontend | React, TypeScript, Vite, and a component library with accessible defaults. |
| Authentication | OIDC-compatible authentication in deployed environments; local development uses a seeded single-user identity with no external secrets. |
| Testing | pytest, Hypothesis, coverage.py, Playwright, and contract tests for broker/data adapters. |
| Quality/security | ruff, mypy, bandit, pip-audit, detect-secrets, container scanning, and dependency lockfiles. |
| Packaging/deployment | uv or locked pip requirements, Docker, Docker Compose, and GitHub Actions-compatible CI. |

## 6. Data Integrity

Every reported result must be tied to an immutable approved data snapshot, code version, feature version, configuration, and exact historical windows. Point-in-time correctness, delistings, corporate actions, and historical universe membership are mandatory.

## 7. Strategy Research and AI Assistance

Allowed families are time-series trend, mean reversion, cross-sectional momentum, volatility/regime filtering, and ML-assisted ranking. AI cannot approve outputs, modify risk rules, access broker secrets, or promote live capital.

## 8. Validation Discipline

| Window | Dates | Use |
| --- | --- | --- |
| In-sample | 2016-01-01 to 2021-12-31 | Hypothesis development. |
| Walk-forward | 2022-01-01 to 2023-12-31 | Selection across at least four chronological folds. |
| Sealed holdout | 2024-01-01 to 2025-12-31 | One final frozen evaluation. |
| Paper trading | At least 60 live market sessions | Forward operational validation. |

| Budget | Limit |
| --- | --- |
| Families | 5 |
| Hypotheses per family | 10 |
| Total trials | 50 |
| Search jobs | 25 |
| Paper candidates | 2 |
| Holdout evaluations | 1 |

## 9. Risk Rules

| Control | Limit or behavior |
| --- | --- |
| Reference NAV | USD 100,000 paper portfolio. |
| Gross exposure | Maximum 100% of NAV. |
| Net exposure | Between 0% and 100% of NAV; long-only. |
| Leverage | Maximum 1.0x; margin borrowing is prohibited. |
| Concurrent positions | Maximum 20. |
| Single-position target | Maximum 7.5% of NAV at order generation and 8.0% hard breach threshold after price movement. |
| Sector exposure | Maximum 25% of NAV using the approved sector classification snapshot. |
| Daily turnover | Maximum 30% of starting NAV, excluding forced risk liquidations. |
| Order participation | Maximum 5% of trailing 20-session average daily share volume and 5% of the current 15-minute bar volume. |
| Minimum price | USD 5.00 at signal timestamp and order submission. |
| Minimum liquidity | Trailing 60-session median daily dollar volume of at least USD 20 million. |
| Daily loss stop | At -2.0% from prior session close, cancel open buy orders and prohibit new exposure until Risk Owner reset. |
| Drawdown stop | At -10.0% from portfolio high-water mark, activate the kill switch and move to a controlled flattening state. |
| Stale data | No new orders when the latest required market bar is more than 2 expected bar intervals late. |
| Slippage alert | Flag any fill worse than the reference price by more than 50 basis points; three such events in five sessions pause new orders. |
| Order window | Regular session only, 09:35 through 15:45 America/New_York. |
| Duplicate protection | A deterministic client order key prevents the same intended order from being submitted twice. |
| Manual control | Risk Owner and authorized operator can pause strategies, cancel orders, or activate the kill switch at any time. |

## 10. Functional Requirements

| ID | Requirement | Verification evidence |
| --- | --- | --- |
| FR-001 | The repository shall treat the approved specification as the source of truth and shall link every implementation task to one or more requirement identifiers. | Traceability check shows every task and changed module mapped to requirement IDs. |
| FR-002 | The system shall maintain maker and checker roles and shall prevent a maker from recording final checker approval for the same production-loop task. | Authorization test rejects self-approval. |
| FR-003 | The project shall record approvals for data snapshots, experiment plans, risk rules, holdout access, and paper-candidate activation. | Approval records contain actor, timestamp, object, decision, and rationale. |
| FR-004 | The project shall maintain STATE.md with current phase, completed tasks, active blockers, trial counts, holdout status, and next approved task. | Automated state lint verifies all required fields are present. |
| FR-005 | The project shall stop iteration when acceptance criteria pass, the trial budget is exhausted, the same failure repeats three times, required information is absent, human approval is required, or another holdout access would be needed. | Workflow tests demonstrate each stop condition blocks further execution. |
| FR-006 | Any change to asset class, jurisdiction, live-capital boundary, risk thresholds, validation windows, or trial budget shall require a spec revision and recorded approval before code changes. | Change-control test rejects execution under mismatched spec/config version. |
| FR-007 | No agent or model shall be authorized to approve its own output, change risk limits, access broker secrets directly, or promote a deployment to live capital. | Policy tests and permission review confirm prohibited capabilities are absent. |
| FR-008 | Every final report shall contain summary, alignment status, verification results, metrics with search-size context, files changed, remaining risks, human approvals, and recommended next step. | Report schema validation passes. |
| FR-009 | The system shall preserve rejected hypotheses and failed trials with the same metadata standards as successful trials. | Registry query confirms failed and rejected records are immutable and complete. |
| FR-010 | Unrelated file changes shall fail checker review unless separately traced to an approved requirement. | Checker checklist and diff scope test detect unrelated changes. |
| FR-011 | The system shall authenticate every non-health-check request. | Unauthenticated request tests return 401. |
| FR-012 | The system shall implement roles for viewer, researcher, operator, checker, risk owner, compliance owner, security owner, and administrator. | Authorization matrix tests cover all protected actions. |
| FR-013 | The system shall enforce least privilege and deny access not explicitly granted. | Negative authorization tests pass. |
| FR-014 | The system shall require step-up confirmation for kill-switch reset, holdout unseal, credential registration, and paper-candidate activation. | Sensitive action tests require a second explicit confirmation event. |
| FR-015 | The system shall record successful and failed authentication events without storing passwords, tokens, or secret material. | Audit log inspection and secret scanner pass. |
| FR-016 | The system shall expire web sessions after 30 minutes of inactivity and require reauthentication after 12 hours. | Session lifecycle tests pass. |
| FR-017 | The system shall support service identities with scoped permissions for workers and scheduled jobs. | Service account tests show no interactive/admin permissions. |
| FR-018 | The system shall disable an identity immediately when an administrator revokes access. | Revocation integration test prevents subsequent requests. |
| FR-019 | The system shall import market data only through registered provider adapters or approved immutable local snapshots. | Unregistered source import is rejected. |
| FR-020 | Every dataset snapshot shall have a unique immutable identifier, provider, license classification, ingestion timestamp, date range, schema version, row count, and SHA-256 manifest checksum. | Manifest schema validation passes. |
| FR-021 | Raw imported files shall be write-once; corrections shall create a new snapshot rather than mutate an existing snapshot. | Mutation attempt fails and replacement creates a new ID. |
| FR-022 | The system shall distinguish event time, provider publication time, ingestion time, and feature availability time. | Schema and point-in-time tests verify all timestamps. |
| FR-023 | The system shall validate symbol, exchange, session date, timezone, open, high, low, close, volume, and adjustment fields. | Invalid-row fixtures are rejected with classified errors. |
| FR-024 | The system shall reject bars with negative prices or volume, high below low, open or close outside the high-low range, duplicate keys, or timestamps outside the expected session. | Property-based validation tests pass. |
| FR-025 | The system shall detect missing sessions against an approved exchange calendar and classify expected holidays separately from data gaps. | Calendar completeness test passes. |
| FR-026 | The system shall store corporate-action events and apply split and dividend adjustments without using information before the event becomes known. | Corporate-action regression fixtures pass. |
| FR-027 | The system shall preserve delisted securities in historical universes and shall not construct a historical universe from current constituents only. | Survivorship-bias test includes delisted fixture symbols. |
| FR-028 | Universe membership shall be generated as of each historical decision timestamp using only available information. | Point-in-time universe test passes. |
| FR-029 | The approved MVP universe shall include only U.S.-listed common stocks and unleveraged ETFs meeting price, liquidity, exchange, and history requirements. | Universe report lists inclusion and exclusion reasons. |
| FR-030 | The system shall quarantine a snapshot when critical validation errors exceed zero or noncritical missing-bar rate exceeds 0.1%. | Quarantine tests and data-quality report pass. |
| FR-031 | The system shall record every transformation from raw snapshot to curated snapshot with code version and input/output checksums. | Lineage graph is complete and reproducible. |
| FR-032 | The system shall support deterministic rebuild of curated data from the same raw snapshot and code version. | Two independent builds produce identical checksums. |
| FR-033 | The system shall prevent a backtest from using a snapshot whose approval status is not approved. | Backtest request with unapproved data is rejected. |
| FR-034 | The system shall expose data freshness, gap rate, duplicate rate, outlier count, and quarantine status in the dashboard. | Dashboard/API contract test returns all metrics. |
| FR-035 | The system shall retain imported raw snapshots and manifests for at least seven years unless licensing terms require earlier deletion. | Retention policy configuration and lifecycle test pass. |
| FR-036 | Each feature definition shall declare inputs, parameters, lookback, expected frequency, availability lag, null policy, and output type. | Feature registry schema validation passes. |
| FR-037 | Feature computation shall be deterministic for a fixed data snapshot, code version, and configuration. | Rebuild produces identical feature checksums. |
| FR-038 | A feature value shall not be available to a strategy before its declared availability timestamp. | Leakage sentinel tests fail intentionally leaky features. |
| FR-039 | Rolling calculations shall require the full declared lookback unless the feature explicitly defines a warm-up policy. | Warm-up tests verify null behavior. |
| FR-040 | Cross-sectional features shall use only securities eligible in the point-in-time universe for the same timestamp. | Universe isolation test passes. |
| FR-041 | Feature artifacts shall be partitioned by snapshot, frequency, and date and stored as immutable Parquet. | Artifact path and immutability tests pass. |
| FR-042 | The feature service shall report null rate, distribution drift, minimum, maximum, mean, standard deviation, and selected quantiles. | Feature-quality report contains required statistics. |
| FR-043 | Feature definitions shall be versioned and historical experiments shall retain the exact version used. | Experiment-to-feature-version traceability passes. |
| FR-044 | No generated natural-language or model-derived feature shall enter a strategy without a deterministic extraction schema and approval. | Unapproved model feature is rejected. |
| FR-045 | Feature jobs shall be idempotent and safe to resume after interruption. | Restart test yields one canonical artifact and no duplicates. |
| FR-046 | Every strategy family shall have a written economic hypothesis, expected failure modes, benchmark, and falsification criteria before its first trial. | Experiment-plan validation rejects missing fields. |
| FR-047 | The initial allowed families shall be time-series trend, mean reversion, cross-sectional momentum, volatility/regime filtering, and ML-assisted ranking. | Registry rejects an unapproved family without spec revision. |
| FR-048 | The experiment registry shall assign a monotonically unique trial ID before computation begins. | Concurrent creation test produces unique IDs. |
| FR-049 | Every trial shall record hypothesis ID, family, parameters, code commit, environment lock hash, data snapshot, feature versions, windows, random seed, start/end timestamps, status, metrics, and artifact references. | Trial completeness validation passes. |
| FR-050 | The system shall enforce the 50-trial total hypothesis budget and 25 parameter-search-job budget. | Budget boundary tests block the next unapproved trial. |
| FR-051 | A search job shall declare its search space and maximum evaluations before execution. | Search request without declared budget is rejected. |
| FR-052 | The system shall count failed, crashed, cancelled, and invalid trials against the trial budget once data-dependent computation begins. | Budget accounting tests pass. |
| FR-053 | Randomized models shall use recorded seeds and deterministic settings where supported. | Reproduction test meets metric tolerance. |
| FR-054 | Strategy code shall emit signals or target weights only and shall have no dependency on broker clients or credentials. | Dependency boundary test passes. |
| FR-055 | Baseline strategies shall be implemented before ML-assisted ranking is eligible for evaluation. | Workflow gate blocks ML family until baseline reports exist. |
| FR-056 | Model training shall use only in-sample and current walk-forward training folds and shall never train on sealed holdout data. | Training dataset lineage test passes. |
| FR-057 | Hyperparameter selection shall use walk-forward validation metrics and shall not inspect the sealed holdout. | Access logs show no holdout reads before unseal. |
| FR-058 | The system shall display the number of prior trials and search jobs beside every reported performance result. | Report/UI schema test passes. |
| FR-059 | Rejected hypotheses shall include a reason and may be revised only through a new hypothesis ID. | Registry immutability test passes. |
| FR-060 | The system shall stop a strategy family after three consecutive failures with the same classified root cause and require hypothesis review. | Failure routing test blocks additional tuning. |
| FR-061 | The backtest engine shall process signals using event-time ordering and shall prohibit fills before an order is eligible. | Temporal ordering tests pass. |
| FR-062 | The default daily strategy shall calculate after the close and execute no earlier than the next regular-session tradable event. | Look-ahead regression test passes. |
| FR-063 | The engine shall model commissions, regulatory fees where applicable, bid-ask cost, market impact, and configurable slippage. | Cost-model unit tests and zero-cost comparison pass. |
| FR-064 | The engine shall reject fills that exceed price limits, available bar volume, order participation limits, or market-session rules. | Impossible-fill fixtures are rejected. |
| FR-065 | The engine shall support market, limit, and cancel instructions for simulation, while the MVP strategy workflow shall use marketable paper orders only. | Order-type tests pass and unsupported types are blocked. |
| FR-066 | Portfolio accounting shall reconcile cash, positions, realized P&L, unrealized P&L, fees, dividends, and corporate actions each event. | Double-entry reconciliation remains balanced. |
| FR-067 | The engine shall benchmark candidates against SPY buy-and-hold and an equal-weight eligible-universe baseline. | Backtest report includes both benchmarks. |
| FR-068 | The engine shall calculate all required performance and risk metrics with documented formulas. | Golden dataset metric tests match independent calculations. |
| FR-069 | The engine shall produce a trade ledger, order ledger, daily equity curve, exposure series, drawdown series, and attribution report. | Artifact completeness validation passes. |
| FR-070 | Backtests shall be deterministic within 1e-9 relative tolerance for identical inputs. | Repeated-run regression test passes. |
| FR-071 | Walk-forward validation shall use expanding or rolling training windows defined in configuration and shall preserve chronology. | Fold-boundary tests pass. |
| FR-072 | The approved validation period shall contain at least four chronological folds and shall report fold-level and aggregate metrics. | Validation report schema and count check pass. |
| FR-073 | The sealed holdout dataset shall be encrypted or access-controlled separately and inaccessible to normal research jobs. | Permission and audit tests pass. |
| FR-074 | Holdout unseal shall require Quant Lead and Checker approvals and shall record the frozen commit, configuration, data snapshot, and artifact hashes. | Unseal workflow test requires both approvals. |
| FR-075 | The system shall permit exactly one holdout evaluation for the frozen finalist under this specification. | Second evaluation attempt is blocked. |
| FR-076 | Holdout failure shall mark the candidate failed and shall not reopen tuning against the same holdout. | State transition test passes. |
| FR-077 | A candidate shall proceed to paper trading only when all data, validation, risk, reproducibility, and checker gates pass. | Release-gate test blocks any failed criterion. |
| FR-078 | Backtest reports shall disclose assumptions, limitations, data snapshot, code commit, windows, and search-size context. | Report lint passes. |
| FR-079 | Capacity analysis shall estimate participation, turnover, and slippage sensitivity at USD 100k, USD 500k, and USD 1m notional. | Capacity report includes all three scenarios. |
| FR-080 | The risk subsystem shall be a separate module from strategy code and shall be invoked before every simulated or paper order. | Architecture and integration tests confirm mandatory call path. |
| FR-081 | Risk configuration shall be versioned, immutable per run, and approved by the Risk Owner. | Run metadata references an approved risk-config hash. |
| FR-082 | The system shall enforce maximum gross exposure of 100% and leverage of 1.0x. | Boundary tests reject excess exposure. |
| FR-083 | The system shall enforce a maximum of 20 concurrent positions. | Twenty-first position test is rejected. |
| FR-084 | The system shall enforce a 7.5% target and 8.0% hard single-position threshold. | Sizing and breach tests pass. |
| FR-085 | The system shall enforce a 25% sector exposure limit. | Sector concentration test is rejected. |
| FR-086 | The system shall enforce a 30% daily turnover limit except for forced risk liquidation. | Turnover boundary test passes. |
| FR-087 | The system shall enforce minimum price and liquidity eligibility before new exposure. | Illiquid and sub-USD-5 fixtures are rejected. |
| FR-088 | The system shall enforce order participation limits against trailing and current volume. | Oversized order test is clipped or rejected according to policy. |
| FR-089 | At a 2.0% session loss, the system shall cancel open buy orders and prohibit new exposure until Risk Owner reset. | Loss-stop scenario test passes. |
| FR-090 | At a 10.0% high-water-mark drawdown, the system shall activate the kill switch and enter controlled flattening. | Drawdown scenario test passes. |
| FR-091 | The system shall prohibit new orders when required market data is stale by more than two expected intervals. | Stale-feed test blocks orders. |
| FR-092 | Three fills with slippage worse than 50 basis points within five sessions shall pause new orders and create an incident. | Rolling-window slippage test passes. |
| FR-093 | The system shall reject duplicate client order keys. | Idempotency test submits exactly one broker order. |
| FR-094 | The system shall allow authorized manual pause, cancel-all, and kill-switch actions independent of strategy health. | Operator control tests pass. |
| FR-095 | A kill-switch reset shall require Risk Owner approval, a resolved incident, healthy data, successful reconciliation, and no active critical alerts. | Reset workflow test rejects incomplete prerequisites. |
| FR-096 | Risk breaches shall be immutable audit events containing inputs, limits, decision, and resulting action. | Audit schema validation passes. |
| FR-097 | No strategy, model, or researcher role shall be able to modify active risk thresholds. | Authorization tests pass. |
| FR-098 | The risk dashboard shall show current exposure, concentration, drawdown, daily P&L, liquidity utilization, active limits, and kill-switch status. | Dashboard/API contract test passes. |
| FR-099 | The broker interface shall expose submit, cancel, replace, list orders, list positions, account state, and streaming or polling reconciliation methods. | Adapter contract tests pass. |
| FR-100 | The Alpaca implementation shall operate only in paper mode under this specification. | Configuration guard rejects live endpoint or live credentials. |
| FR-101 | Broker credentials shall be loaded from the deployment secret store and shall never be stored in source, database fields, experiment artifacts, or logs. | Secret scanning and runtime log tests pass. |
| FR-102 | Paper orders shall be created only from an approved candidate, approved risk configuration, current approved data, and healthy system state. | Order gate integration tests pass. |
| FR-103 | The system shall submit orders only during 09:35-15:45 America/New_York regular sessions. | Session-time tests pass including daylight-saving transitions. |
| FR-104 | Every paper order shall have a deterministic client order key derived from candidate, rebalance timestamp, symbol, side, and intent version. | Repeat generation produces the same key. |
| FR-105 | The system shall persist intended orders before broker submission and persist broker acknowledgements after submission. | Crash-recovery test reconciles the indeterminate state. |
| FR-106 | The system shall reconcile internal orders, broker orders, positions, cash, and fills at least every minute while active and once after the close. | Scheduler and reconciliation tests pass. |
| FR-107 | Any unexplained broker position, order, or cash discrepancy shall pause new orders and create a critical incident. | Injected discrepancy scenario activates pause. |
| FR-108 | Order rejection shall be classified, audited, surfaced, and shall not be retried automatically unless the reason is explicitly retryable. | Rejection-policy tests pass. |
| FR-109 | Network timeouts shall use idempotent reconciliation before any retry. | Timeout simulation produces no duplicate order. |
| FR-110 | The system shall support cancel-all and controlled flattening in paper mode. | End-to-end paper sandbox test passes. |
| FR-111 | Paper trading shall run for at least 60 live market sessions before any live-capital proposal may be authored. | Gate checks session count and unresolved incidents. |
| FR-112 | Paper-trading reports shall compare expected signals, intended orders, broker orders, fills, positions, costs, and P&L daily. | Daily reconciliation report is complete. |
| FR-113 | No automated process shall convert paper configuration, endpoints, or credentials to live mode. | Static and runtime guards pass. |
| FR-114 | A live-trading request shall create a new project specification rather than alter this MVP configuration. | Change-control test routes request to a new spec. |
| FR-115 | The system shall generate HTML, JSON, and PDF-compatible reports from canonical structured results. | Report generation tests produce all formats. |
| FR-116 | Every report shall identify specification version, code commit, environment lock, data snapshot, feature versions, risk config, and generation timestamp. | Report metadata lint passes. |
| FR-117 | Experiment comparison shall prohibit comparing metrics computed with incompatible windows, data snapshots, or cost assumptions without an explicit warning. | Comparison compatibility test passes. |
| FR-118 | The dashboard shall display trial budget used and remaining by family and total. | API/UI tests pass. |
| FR-119 | The dashboard shall display holdout status as sealed, authorized, evaluated, or retired. | State transition UI test passes. |
| FR-120 | The system shall alert on failed jobs, stale data, risk breaches, reconciliation discrepancies, paper-order rejection clusters, and service health failures. | Alert-routing tests pass. |
| FR-121 | Alerts shall have severity, owner, deduplication key, first/last occurrence, acknowledgement, and resolution. | Alert schema validation passes. |
| FR-122 | Critical alerts shall pause new paper orders when the affected subsystem can compromise order correctness or risk control. | Critical-alert scenario test passes. |
| FR-123 | Operational metrics shall include job latency, queue depth, API error rate, data freshness, reconciliation lag, order latency, and risk-check latency. | Metrics endpoint exposes all required series. |
| FR-124 | Audit events shall be searchable by actor, event type, object, time range, and correlation ID. | Audit search integration test passes. |
| FR-125 | The system shall export a final report matching the project final-report template. | Template conformance test passes. |
| FR-126 | The system shall retain audit events and final reports for seven years. | Retention policy test passes. |
| FR-127 | The system shall provide a downloadable evidence bundle containing configs, manifests, metrics, ledgers, approvals, and checksums for a selected run. | Evidence-bundle test verifies completeness and checksums. |
| FR-128 | The system shall use TLS for external network communication in deployed environments. | Deployment configuration and scan confirm TLS. |
| FR-129 | Secrets shall be supplied through a secret manager or protected environment injection and shall never have default production values. | Configuration validation and secret scan pass. |
| FR-130 | The system shall encrypt sensitive persisted configuration and credential references at rest. | Storage configuration and integration test pass. |
| FR-131 | The system shall validate all API inputs and reject unknown fields for security-sensitive commands. | Fuzz and schema tests pass. |
| FR-132 | The system shall use parameterized database access and shall prohibit dynamic SQL from user input. | Static analysis and injection tests pass. |
| FR-133 | File imports shall enforce type, size, checksum, schema, and path-safety controls. | Malicious upload fixtures are rejected. |
| FR-134 | Dependencies shall be pinned and scanned on every pull request and release build. | CI evidence includes dependency scan. |
| FR-135 | Critical or high known vulnerabilities with a practical exploit path shall block release unless the Security Owner records a time-bounded exception. | Release gate test passes. |
| FR-136 | Logs shall redact authorization headers, cookies, tokens, credentials, and configured sensitive fields. | Log redaction tests pass. |
| FR-137 | The system shall produce tamper-evident audit chains using event hashes or immutable object-lock storage. | Integrity verification detects modified events. |
| FR-138 | Backups shall be encrypted, tested quarterly, and excluded from developer workstations. | Restore exercise evidence and configuration review pass. |
| FR-139 | The system shall maintain an incident record for security, data integrity, risk, and execution events. | Incident schema and workflow tests pass. |
| FR-140 | Administrative actions shall require explicit reason text and be included in the audit trail. | Admin action without reason is rejected. |

## 11. Non-Functional Requirements

| ID | Requirement | Verification evidence |
| --- | --- | --- |
| NFR-001 | A ten-year daily backtest over 3,000 symbols shall complete within 10 minutes on an 8-core, 32 GB reference machine. | Performance benchmark in CI or scheduled benchmark environment. |
| NFR-002 | A five-year 15-minute backtest over 500 symbols shall complete within 30 minutes on the reference machine. | Performance benchmark report. |
| NFR-003 | Pre-trade risk evaluation shall have p95 latency below 50 ms and p99 below 100 ms excluding external broker calls. | Load test results. |
| NFR-004 | Metadata API reads shall have p95 latency below 500 ms at 25 concurrent users. | API load test. |
| NFR-005 | Order intent persistence plus risk decision shall complete before broker submission and shall be recoverable after process termination. | Crash-consistency integration test. |
| NFR-006 | The paper-trading service shall target 99.5% availability during regular market hours, excluding scheduled maintenance. | Monthly availability report. |
| NFR-007 | Critical data, risk, and reconciliation alerts shall be emitted within 60 seconds of detection. | Alert latency test. |
| NFR-008 | The platform shall recover metadata with RPO of 15 minutes and RTO of 2 hours. | Backup/restore exercise. |
| NFR-009 | Immutable data and artifact snapshots shall have RPO of zero after successful commit. | Object-store durability and checksum verification. |
| NFR-010 | All timestamps shall be stored in UTC and displayed with explicit timezone; exchange logic shall use America/New_York. | Timezone and daylight-saving tests. |
| NFR-011 | Critical risk, accounting, and point-in-time modules shall have at least 95% branch coverage; the repository overall shall have at least 85%. | Coverage report. |
| NFR-012 | Type checking shall pass with no errors for production Python modules. | mypy CI result. |
| NFR-013 | Linting and formatting checks shall pass with no ignored new violations. | ruff CI result. |
| NFR-014 | The codebase shall run on Linux x86_64 and arm64 containers. | Multi-architecture build test. |
| NFR-015 | All public API endpoints shall be versioned under /api/v1. | OpenAPI contract test. |
| NFR-016 | Database migrations shall be forward-only in deployed environments and tested from the previous released schema. | Migration integration test. |
| NFR-017 | Jobs shall be idempotent and at-least-once execution shall not create duplicate canonical artifacts or orders. | Retry and duplicate tests. |
| NFR-018 | Every log and event shall include correlation ID, environment, service, version, and timestamp. | Structured log schema test. |
| NFR-019 | No secret or credential pattern shall be present in git history or built artifacts. | detect-secrets and artifact scan. |
| NFR-020 | The user interface shall meet WCAG 2.1 AA for core workflows. | Automated accessibility scan and manual keyboard review. |
| NFR-021 | The system shall support at least 100,000 experiment records and 10 million audit events without changing the logical architecture. | Scale test and query plan review. |
| NFR-022 | Experiment records, manifests, approvals, and audit events shall be immutable after finalization. | Mutation tests and database constraints. |
| NFR-023 | Reports shall be reproducible from structured artifacts without re-running a strategy. | Report rebuild test. |
| NFR-024 | Numerical calculations shall use documented precision and avoid binary floating-point for cash ledger amounts. | Accounting precision tests. |
| NFR-025 | All external adapters shall have timeouts, bounded retries, circuit breakers, and contract tests. | Failure-injection tests. |
| NFR-026 | The system shall fail closed for authorization, risk checks, data approval, and holdout access. | Negative-path integration tests. |
| NFR-027 | Deployment configuration shall be environment-specific and validated at startup. | Invalid-config startup tests. |
| NFR-028 | The repository shall contain no production credential examples; examples shall use non-secret syntactically invalid values. | Secret scan and config review. |
| NFR-029 | A new developer shall be able to start the local stack and run the test suite using documented commands on a clean machine. | Onboarding smoke test. |
| NFR-030 | The local test suite excluding performance tests shall complete within 15 minutes on the reference machine. | CI duration report. |
| NFR-031 | The system shall preserve backward readability of released experiment and manifest schemas through explicit migration utilities. | Fixture compatibility tests. |
| NFR-032 | All data and configuration schemas shall include semantic versions. | Schema lint. |
| NFR-033 | The dashboard shall display degraded mode clearly and shall not imply that stale information is current. | UI stale-state tests. |
| NFR-034 | The system shall use deterministic sorting and stable identifiers in reports to support exact diffs. | Snapshot regression tests. |
| NFR-035 | Release artifacts shall include software bill of materials, dependency lock, image digest, and signed checksum. | Release pipeline evidence. |

## 12. Acceptance Scenarios

| ID | Scenario | Given | When | Then |
| --- | --- | --- | --- | --- |
| SC-001 | Import an approved snapshot | a licensed historical bar export and provider metadata are available | the Data Owner imports and validates the files | the system writes immutable raw artifacts, a manifest, quality results, and an approval-ready curated snapshot without mutating prior data |
| SC-002 | Run a baseline backtest | an approved snapshot, approved feature set, and registered baseline strategy exist | a Researcher starts a backtest | the system reserves a trial ID, enforces budget, runs deterministically, stores ledgers and metrics, and reports search-size context |
| SC-003 | Run walk-forward validation | a candidate passes in-sample quality checks | the Quant Lead authorizes validation | the system executes chronological folds, reports fold dispersion, and does not read sealed holdout data |
| SC-004 | Approve holdout evaluation | one frozen finalist exists with code, config, data, and risk hashes | the Quant Lead and Checker approve unsealing | the system records both approvals and permits exactly one holdout run |
| SC-005 | Promote to paper candidate | the frozen candidate passes all release gates | the Risk Owner and Checker activate it | the system creates a paper-candidate version tied to immutable artifacts and enables paper-order generation only |
| SC-006 | Generate a rebalance | the approved candidate has fresh data and the market is within the allowed window | the scheduled rebalance runs | the system computes targets, applies portfolio and risk constraints, persists order intents, and submits idempotent paper orders |
| SC-007 | Reconcile paper trading | paper orders and broker state exist | the reconciliation job runs | the system matches orders, fills, cash, and positions and publishes a complete reconciliation report |
| SC-008 | Manual strategy pause | a strategy is active in paper mode | an authorized Operator pauses it with a reason | the system prohibits new orders, leaves risk monitoring active, and writes an audit event |
| SC-009 | Build an evidence bundle | a completed experiment or paper session exists | a Checker requests evidence | the system exports manifests, configs, approvals, ledgers, metrics, logs, and checksums in a reproducible bundle |
| SC-010 | Resume an interrupted job | a feature or backtest job stops after partial work | the worker restarts | the system resumes or safely re-runs idempotently and produces one canonical finalized artifact |
| SC-011 | Compare experiments | two experiments use compatible windows, data, and costs | a Researcher opens comparison | the system displays metrics, trial counts, parameter differences, and uncertainty without hiding failed folds |
| SC-012 | Complete maker-checker review | a Maker finishes an assigned task with tests and state updates | an independent Checker reviews it | the system records acceptance or rejection with traceability and blocks self-approval |

## 13. Adverse Scenarios

| ID | Scenario | Given | When | Then |
| --- | --- | --- | --- | --- |
| ADV-001 | Look-ahead feature detected | a feature uses a value before its availability timestamp | point-in-time tests run | the tests fail, the feature artifact is rejected, and related trials are invalidated |
| ADV-002 | Survivorship-biased universe | a historical universe is built from current constituents only | data-integrity checks run | the build is quarantined and cannot be approved for backtesting |
| ADV-003 | Stale market data | required bars are more than two intervals late | a rebalance attempts to run | the system blocks new orders, emits a critical alert, and records the stale inputs |
| ADV-004 | Duplicate order retry | a broker request times out after accepting an order | the worker retries | the system reconciles by deterministic client key and does not create a second order |
| ADV-005 | Unexpected broker position | the broker reports a position absent from internal state | reconciliation runs | the system pauses new orders, creates a critical incident, and requires operator resolution |
| ADV-006 | Daily loss breach | session P&L reaches -2.0% | risk monitoring updates | open buy orders are cancelled and new exposure is prohibited until Risk Owner reset |
| ADV-007 | Drawdown kill switch | portfolio drawdown reaches -10.0% from high-water mark | risk monitoring updates | the kill switch activates and controlled flattening begins |
| ADV-008 | Trial budget exhausted | 50 data-dependent hypothesis trials have been consumed | a Researcher requests another trial | the system rejects it until an approved specification revision changes the budget |
| ADV-009 | Repeated holdout access | the finalist holdout has already been evaluated | another holdout job is requested | the system rejects the request and marks the holdout retired |
| ADV-010 | Secret appears in logs | an adapter error contains an authorization header | the logger processes the event | the value is redacted and secret-scanning tests verify no secret persisted |
| ADV-011 | Unapproved risk change | a Researcher edits active position limits | the configuration is submitted | authorization and approval checks reject the change |
| ADV-012 | Live endpoint configured | an environment is configured with a live broker endpoint | the MVP service starts | startup fails closed and identifies the prohibited live configuration |
| ADV-013 | Corporate-action correction | a provider corrects a historical split record | the Data Owner imports the correction | the system creates a new snapshot, preserves the prior snapshot, and identifies affected experiments |
| ADV-014 | Broker connection failure | the paper broker is unavailable | an order window opens | the system queues no blind retries, pauses new submissions, and reconciles when connectivity returns |
| ADV-015 | Excessive slippage cluster | three fills exceed 50 basis points adverse slippage within five sessions | the third event is recorded | new orders pause and an incident requires Risk Owner review |
| ADV-016 | Same failure repeated three times | three consecutive trials fail for the same root cause | another tuning run is requested | the workflow stops the family and requires hypothesis review |

## 14. Release Gates

| Gate | Pass condition |
| --- | --- |
| G1 Specification | Constitution and feature spec are approved; all requirements are measurable; no code conflicts with the spec. |
| G2 Data | Snapshot is approved, immutable, point-in-time correct, reproducible, and passes quality thresholds. |
| G3 Infrastructure | Backtest, experiment registry, risk engine, audit logging, and evidence bundles pass integration tests. |
| G4 Research discipline | Trial budget is not exceeded; every trial is logged; baseline families precede ML; no holdout access occurred. |
| G5 Walk-forward | Candidate has positive net return in at least 60% of folds, aggregate OOS Sharpe at least 0.80, no single fold drawdown above 12%, and stable cost sensitivity. |
| G6 Risk | All adverse risk scenarios pass; max drawdown is at most 10% in approved validation; position, sector, liquidity, and turnover limits are satisfied. |
| G7 Holdout freeze | Code, parameters, data, features, cost model, and risk rules are frozen and hashed; Quant Lead and Checker approve one access. |
| G8 Sealed holdout | Net return after costs is positive, Sharpe is at least 0.80, maximum drawdown is at most 10%, and no integrity or risk gate fails. |
| G9 Paper activation | Risk Owner and Checker approve the frozen candidate; paper endpoint and credentials are verified; kill-switch and reconciliation drills pass. |
| G10 Paper completion | At least 60 live market sessions, no unexplained orders, no unresolved critical incidents, no unapproved risk breach, and complete daily reconciliation. |

## 15. Verification Commands

```bash
pytest
ruff check .
mypy .
python -m backtest --config specs/ai-trading-mvp/config.yaml
python -m walk_forward --config specs/ai-trading-mvp/config.yaml
python -m sim --config specs/ai-trading-mvp/config.yaml
python -m risk_checks --config specs/ai-trading-mvp/config.yaml
```

## 16. Roadmap

| Phase | Duration | Work | Exit |
| --- | --- | --- | --- |
| Phase 0 - Repository bootstrap | 1 week | Install Spec Kit, adopt constitution, add this PRD, create feature spec/plan/tasks/state, configure CI. | Approved controlling artifacts and green bootstrap checks. |
| Phase 1 - Data foundation | 2 weeks | Implement schemas, provider interfaces, immutable snapshots, manifests, quality checks, calendars, and corporate actions. | Approved reproducible sample snapshot; point-in-time and survivorship tests pass. |
| Phase 2 - Experiment and backtest core | 3 weeks | Implement feature registry, trial registry, deterministic engine, costs, accounting, benchmarks, and reports. | Golden backtests reproduce; trial budget enforcement and evidence bundles pass. |
| Phase 3 - Validation and baseline strategies | 3 weeks | Implement walk-forward engine and four interpretable baseline families; run bounded research. | Candidate review report with all trials and no holdout access. |
| Phase 4 - Risk and paper adapter | 3 weeks | Implement portfolio constraints, risk engine, Alpaca paper adapter, idempotency, reconciliation, and kill switch. | All adverse risk/execution scenarios pass in sandbox. |
| Phase 5 - Frozen candidate and holdout | 1 week | Freeze one finalist and execute the single sealed holdout after dual approval. | Pass/fail holdout report with search-size context. |
| Phase 6 - Paper trading | Minimum 60 market sessions | Operate the approved candidate, reconcile daily, monitor risk and incidents, and issue weekly reports. | Paper completion gate passes or candidate is retired. |
| Phase 7 - Final decision | 1 week | Complete technical, risk, compliance, security, and product review. | Decision to continue research, extend paper trading, productize the platform, or halt. |

## 17. Traceable Tasks

| ID | Task | Implementation | Acceptance |
| --- | --- | --- | --- |
| T001 | Adopt project constitution | Create .specify/memory/constitution.md from the governance rules in this document. | Constitution review passes. |
| T002 | Create feature spec | Create specs/ai-trading-mvp/spec.md with requirements and scenarios. | Spec lint and Product Owner approval. |
| T003 | Create implementation plan | Create plan.md with architecture, interfaces, migrations, and test strategy. | Checker confirms full requirement coverage. |
| T004 | Create traceable tasks | Create tasks.md mapping each task to FR/NFR/scenario IDs. | No orphan requirement or task. |
| T005 | Create STATE.md | Record phase, approvals, budgets, holdout state, and next task. | State lint passes. |
| T006 | Create config schema | Implement versioned typed configuration and the baseline YAML in this document. | Invalid config tests pass. |
| T007 | Bootstrap CI | Add pytest, ruff, mypy, security scans, coverage gates, and build checks. | Pull request pipeline is green. |
| T008 | Create domain models | Implement identifiers, timestamps, money, quantities, orders, positions, metrics, and audit event types. | Unit and property tests pass. |
| T009 | Implement PostgreSQL schema | Add migrations for users, approvals, datasets, features, trials, jobs, orders, incidents, and audits. | Migration tests pass from empty and prior schema. |
| T010 | Implement artifact store | Add content-addressed immutable object paths and checksums. | Mutation and checksum tests pass. |
| T011 | Implement data provider interface | Create HistoricalBarProvider and LocalParquetProvider. | Contract tests pass. |
| T012 | Implement snapshot manifests | Create manifest generation, signing/checksum, and approval status. | Manifest schema and reproduction tests pass. |
| T013 | Implement market calendar | Add U.S. exchange sessions and timezone handling. | Holiday and DST fixtures pass. |
| T014 | Implement data validation | Add OHLCV, duplicate, gap, outlier, and schema checks. | Invalid fixtures are correctly classified. |
| T015 | Implement corporate actions | Add split, dividend, symbol-change, and delisting handling. | Regression fixtures pass. |
| T016 | Implement point-in-time universe | Create eligibility computation from historical information only. | Survivorship and availability tests pass. |
| T017 | Implement feature registry | Add feature specifications, versions, availability lags, and dependency graph. | Registry validation passes. |
| T018 | Implement feature runner | Build deterministic partitioned feature artifacts. | Repeated build checksum matches. |
| T019 | Implement feature quality report | Add null, distribution, drift, and outlier metrics. | Report completeness test passes. |
| T020 | Implement experiment registry | Reserve IDs and persist immutable trial metadata before execution. | Concurrency and completeness tests pass. |
| T021 | Implement budget enforcement | Track family, trial, and search budgets including failed runs. | Boundary tests pass. |
| T022 | Implement hypothesis workflow | Require economic thesis, benchmark, failure modes, and falsification criteria. | Incomplete plans are rejected. |
| T023 | Implement order/event model | Create temporal order lifecycle and event sequencing. | Ordering property tests pass. |
| T024 | Implement portfolio accounting | Track cash, positions, fees, dividends, and P&L with decimal precision. | Ledger balances on golden scenarios. |
| T025 | Implement fill simulator | Add session rules, volume limits, spread, impact, and slippage. | Impossible fills are rejected. |
| T026 | Implement cost model | Create versioned configurable cost assumptions. | Independent formula tests pass. |
| T027 | Implement benchmark engine | Add SPY and equal-weight universe benchmarks. | Benchmark reports match fixtures. |
| T028 | Implement metrics engine | Calculate required performance, risk, capacity, and exposure metrics. | Golden metric tests pass. |
| T029 | Implement report artifacts | Produce ledgers, curves, attribution, HTML, JSON, and PDF-compatible output. | Artifact schema tests pass. |
| T030 | Implement walk-forward engine | Create chronological folds and training/validation isolation. | Fold-boundary tests pass. |
| T031 | Implement holdout vault | Separate access, dual approval, freeze hashes, and one-run enforcement. | Permission and second-run rejection tests pass. |
| T032 | Implement trend baseline | Add predeclared time-series trend family. | Family tests and baseline report pass. |
| T033 | Implement mean-reversion baseline | Add predeclared mean-reversion family. | Family tests and baseline report pass. |
| T034 | Implement cross-sectional momentum | Add ranking and constrained portfolio construction. | Family tests and baseline report pass. |
| T035 | Implement regime filter | Add volatility/regime gating without broker access. | Family tests and baseline report pass. |
| T036 | Implement ML ranking gate | Add ML-assisted family only after baseline completion. | Workflow gate and leakage tests pass. |
| T037 | Implement risk configuration | Version and approve immutable risk rules. | Unauthorized modification tests pass. |
| T038 | Implement pre-trade checks | Enforce exposure, position, sector, liquidity, turnover, and session limits. | Boundary and property tests pass. |
| T039 | Implement P&L stops | Add daily loss and drawdown state transitions. | Adverse scenarios pass. |
| T040 | Implement stale-data controls | Block orders when freshness requirements fail. | Stale-feed scenario passes. |
| T041 | Implement slippage controls | Track rolling slippage breaches and incidents. | Cluster scenario passes. |
| T042 | Implement kill switch | Add independent pause, cancel-all, controlled flatten, and reset workflow. | Drill passes end to end. |
| T043 | Implement broker interface | Create contract for paper broker operations and reconciliation. | Contract tests pass. |
| T044 | Implement Alpaca paper adapter | Add paper-only configuration guard and request mapping. | Sandbox tests pass; live endpoint rejected. |
| T045 | Implement order idempotency | Persist intent and deterministic client order keys. | Timeout retry creates one order. |
| T046 | Implement broker reconciliation | Compare orders, fills, positions, cash, and internal state. | Injected discrepancy pauses trading. |
| T047 | Implement incident workflow | Add severity, ownership, acknowledgement, resolution, and evidence. | Workflow tests pass. |
| T048 | Implement audit chain | Write append-only tamper-evident audit events. | Tamper detection test passes. |
| T049 | Implement authentication and RBAC | Add OIDC integration boundary and local seeded identity. | Authorization matrix passes. |
| T050 | Implement secret handling | Use environment/secret injection and log redaction. | Secret scans and redaction tests pass. |
| T051 | Implement API v1 | Expose datasets, features, experiments, runs, risk, orders, incidents, and evidence endpoints. | OpenAPI contract tests pass. |
| T052 | Implement dashboard shell | Add authenticated navigation and status overview. | Accessibility and smoke tests pass. |
| T053 | Implement experiment dashboard | Show trial status, metrics, budgets, and comparisons. | UI contract tests pass. |
| T054 | Implement risk dashboard | Show limits, exposures, drawdown, incidents, and kill switch. | UI contract tests pass. |
| T055 | Implement paper dashboard | Show signals, intended orders, broker state, fills, and reconciliation. | UI contract tests pass. |
| T056 | Implement alerting | Route health, data, risk, execution, and reconciliation alerts. | Alert latency and dedup tests pass. |
| T057 | Implement backups | Configure encrypted metadata backups and restore test. | RPO/RTO exercise passes. |
| T058 | Implement evidence bundles | Export checksummed approval and result packages. | Checker validates bundle completeness. |
| T059 | Run full security review | Execute dependency, secret, container, input, and authorization testing. | No unaccepted high/critical findings. |
| T060 | Run full data-integrity review | Verify lineage, point-in-time correctness, actions, delistings, and reproducibility. | Data Owner and Checker approve. |
| T061 | Execute bounded research plan | Run no more than the approved trial/search budget. | Registry count and family review complete. |
| T062 | Freeze finalist | Record immutable commit, config, data, feature, cost, and risk hashes. | Freeze manifest approved. |
| T063 | Execute sealed holdout once | Run the authorized holdout and retire access. | Pass/fail report and audit record. |
| T064 | Activate paper candidate | Require Risk Owner and Checker approvals and successful drills. | Candidate active only in paper mode. |
| T065 | Operate 60-session paper trial | Run, monitor, reconcile, and report every market session. | Paper completion gate report. |
| T066 | Produce final report | Complete the mandated final report with all evidence and remaining risks. | All required sections and approvals present. |

## 18. Spec Kit Repository Mapping

```text
docs/AI_TRADING_MASTER_PRD.md
.specify/memory/constitution.md
specs/ai-trading-mvp/spec.md
specs/ai-trading-mvp/plan.md
specs/ai-trading-mvp/tasks.md
specs/ai-trading-mvp/STATE.md
specs/ai-trading-mvp/config.yaml
reports/ai-trading-mvp/final_report.md
```

## Appendix A - Baseline Configuration

```yaml
schema_version: 1.0.0
project:
  id: ai-trading-mvp
  mode: paper_only
  jurisdiction: US
  reference_nav_usd: 100000
universe:
  security_types: [common_stock, unleveraged_etf]
  exchanges: [NYSE, NASDAQ, NYSE_ARCA]
  minimum_price_usd: 5.0
  minimum_median_dollar_volume_60d_usd: 20000000
  minimum_history_sessions: 252
  exclude_otc: true
  exclude_leveraged_and_inverse_etfs: true
data:
  provider: local_parquet
  raw_immutable: true
  manifest_hash: sha256
  frequencies: [1d, 15m]
  timezone_storage: UTC
  exchange_timezone: America/New_York
validation:
  in_sample: [2016-01-01, 2021-12-31]
  walk_forward: [2022-01-01, 2023-12-31]
  sealed_holdout: [2024-01-01, 2025-12-31]
  minimum_walk_forward_folds: 4
  maximum_strategy_families: 5
  maximum_hypotheses_per_family: 10
  maximum_total_trials: 50
  maximum_parameter_search_jobs: 25
  maximum_paper_candidates: 2
  sealed_holdout_evaluations: 1
acceptance:
  minimum_oos_sharpe: 0.80
  minimum_positive_fold_fraction: 0.60
  maximum_validation_drawdown: 0.10
  positive_net_return_after_costs: true
portfolio:
  long_only: true
  maximum_positions: 20
  maximum_target_position_fraction: 0.075
  hard_position_breach_fraction: 0.08
  maximum_sector_fraction: 0.25
  maximum_gross_exposure: 1.0
  maximum_leverage: 1.0
  maximum_daily_turnover_fraction: 0.30
risk:
  daily_loss_stop_fraction: 0.02
  drawdown_kill_fraction: 0.10
  maximum_adv_participation_fraction: 0.05
  maximum_bar_participation_fraction: 0.05
  stale_data_intervals: 2
  slippage_alert_bps: 50
  slippage_pause_count: 3
  slippage_window_sessions: 5
execution:
  adapter: alpaca_paper
  live_endpoints_allowed: false
  regular_session_only: true
  order_window_new_york: [09:35, 15:45]
  reconciliation_interval_seconds: 60
paper_trial:
  minimum_live_market_sessions: 60
security:
  secrets_in_source_allowed: false
  audit_retention_years: 7
  require_dual_approval_for_holdout: true
  require_risk_owner_for_kill_reset: true
```

## Appendix B - Final Report Sections

- Summary
- Alignment Status
- Specification Coverage
- Verification Results
- Data Snapshot and Reproducibility
- Experiment Inventory and Trial/Search Counts
- Backtest Results
- Walk-Forward Results
- Sealed Holdout Results
- Paper-Trading Results
- Reported Metrics With Search-Size Context
- Risk Review
- Compliance Review
- Security Review
- Operational Incidents
- Files Changed
- Remaining Risks
- Human Approval Required
- Recommended Next Step

## Appendix C - Source Basis

This specification synthesizes the project-owner-supplied “AI Trading Project Plan - v0” and “Comprehensive Deep Research Plan.” Draft values and unresolved items in those source documents are resolved here as explicit MVP design decisions. Profitability remains unproven until the defined validation and paper-trading gates pass.