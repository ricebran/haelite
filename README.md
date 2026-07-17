# haelite

Governed research and paper-trading platform scaffolding for the Phase 1 setup work.

## Quickstart

For the full end-to-end validation workflow, follow the feature quickstart in [specs/001-paper-trading-platform/quickstart.md](specs/001-paper-trading-platform/quickstart.md).

## Local development

1. Create a Python virtual environment and install dependencies.
2. Run `./scripts/seed-dev-identity.sh` to create a local `.env` file.
3. Start the local services with `docker compose up -d`.
4. Verify the health endpoint at `http://localhost:8000/health`.
