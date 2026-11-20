#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -f "apps/web/dist/index.html" ]; then
  if command -v pnpm >/dev/null 2>&1; then
    pnpm --dir apps/web build
  else
    npm --prefix apps/web run build
  fi
fi

if [ -x ".venv/bin/uvicorn" ]; then
  UVICORN=".venv/bin/uvicorn"
else
  UVICORN="uvicorn"
fi

echo "Starting ProofForge 3D offline single-process demo at http://127.0.0.1:8000"
exec "$UVICORN" apps.api.main:app --host 127.0.0.1 --port 8000
