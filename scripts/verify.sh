#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -x ".venv/bin/python" ]; then
  PY=".venv/bin/python"
  RUFF=".venv/bin/ruff"
  PYTEST=".venv/bin/pytest"
else
  PY="python3"
  RUFF="ruff"
  PYTEST="pytest"
fi

if command -v pnpm >/dev/null 2>&1; then
  pnpm --dir apps/web typecheck
  pnpm --dir apps/web build
  pnpm --dir apps/web test
else
  npm --prefix apps/web run typecheck
  npm --prefix apps/web run build
  npm --prefix apps/web test
fi

"$RUFF" check apps/api scenarios sandbox-agent
"$PYTEST" apps/api -v
echo "VERIFY_OK"
