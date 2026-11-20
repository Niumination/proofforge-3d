#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
(python3 -m uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 &) 
(pnpm --dir apps/web dev --port 5173 &)
wait
