#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

cat > "$ENV_FILE" <<'EOF'
# Local development configuration for haelite
APP_ENV=development
DATABASE_URL=postgresql+psycopg2://haelite:haelite@localhost:5432/haelite
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
DEV_USER_ID=local-dev-user
DEV_ROLE=researcher
EOF

chmod +x "$ENV_FILE"
echo "Created $ENV_FILE"
