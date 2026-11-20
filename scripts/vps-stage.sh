#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

echo "[VPS-STAGE] Installing Python dependencies into isolated .venv..."
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
.venv/bin/pip install --quiet -e "./apps/api[dev]"

echo "[VPS-STAGE] Installing & building Web Cockpit..."
if command -v pnpm >/dev/null 2>&1; then
  pnpm --dir apps/web install
else
  npm --prefix apps/web install
fi

echo "[VPS-STAGE] Running full verification suite..."
bash scripts/verify.sh

echo "[VPS-STAGE] Starting temporary server for live TCP/SSE E2E smoke test..."
.venv/bin/uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null || true' EXIT

for _ in $(seq 1 30); do
  if curl -fsS http://127.0.0.1:8000/api/health >/dev/null 2>&1; then
    break
  fi
  sleep 0.5
done

.venv/bin/python scripts/smoke_e2e.py --base-url http://127.0.0.1:8000 --require-ui
echo "[VPS-STAGE] Staging verification COMPLETE. Start persistent demo with scripts/demo-offline.sh or systemd unit."
