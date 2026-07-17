# quickstart.md

**Feature**: Governed Research and Paper-Trading Platform
**Purpose**: Runnable validation scenarios to prove the feature works end-to-end

## Prerequisites
- Docker and Docker Compose installed
- Local development credentials configured for the seeded local identity
- (Operational) an approved data snapshot manifest available in the artifact store

## Validation Scenario: Create → Validate → Activate Candidate

1. Start the local stack

```bash
docker compose up -d
```

2. Verify health

```bash
curl http://localhost:8000/health
```

3. Register a data snapshot (operational step: ensure manifest uploaded to artifact store)

4. Create a hypothesis via the API or dashboard

5. Start a validation run referencing the approved snapshot

6. After the run completes, record Quant Lead, Risk Owner, and explicit Checker approvals.

7. Activate the paper candidate (API: `POST /api/v1/candidates/{id}/activate`) and ensure activation fails when any required approval is absent.

8. Run reconciliation and verify the evidence bundle contains the manifests, ledgers, and approvals

## Quick verification checklist
- [ ] Health endpoint returns OK
- [ ] Snapshot manifest registered and approved
- [ ] Validation run completes and artifacts created
- [ ] Approvals recorded for Quant Lead, Risk Owner, and Checker
- [ ] Candidate activation fails when any required approval is absent
- [ ] Candidate activated and evidence bundle retrievable

## Notes
- This guide validates end-to-end behavior but omits detailed operational steps for licensing and broker credential onboarding, which are prerequisites.
