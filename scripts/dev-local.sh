#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 --reload &
API_PID=$!
trap 'kill $API_PID 2>/dev/null || true' EXIT
npm --prefix apps/web run dev
