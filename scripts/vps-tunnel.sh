#!/usr/bin/env bash
set -euo pipefail
# LightVela VPS rule (AGENTS.md): ALWAYS force --protocol http2 for cloudflared.
exec cloudflared tunnel --protocol http2 --url http://127.0.0.1:8000
