#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
pnpm --dir apps/web typecheck
pnpm --dir apps/web build
ruff check apps/api scenarios sandbox-agent scripts
pytest apps/api -q
echo "VERIFY_OK"
