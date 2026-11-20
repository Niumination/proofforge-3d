# ProofForge 3D — Phase 2 Staging & Pre-Flight Overlay (`PF-015`..`PF-018`)

Paket ini melanjutkan Phase 1 (`f5fb2a2`) menuju kesiapan demo & staging panggung NYC (tetap menjaga Phase 3 AI calls terkunci hingga Hari-H 21 Nov 2026).

## Fitur Utama Paket Phase 2

1. **Fix `apps/api/pyproject.toml`**: menambahkan `[tool.setuptools.packages.find]` (`where = ["../.."]`, `include = ["apps*", "scenarios*"]`) — memperbaiki error `Multiple top-level packages discovered in a flat-layout` saat `pip install -e "./apps/api[dev]"`.
2. **Single-Process Offline + Tunnel Mode (`apps/api/main.py`)**: otomatis melayani bundle produksi `apps/web/dist` di `http://127.0.0.1:8000` bersama seluruh endpoint `/api/*` dan SSE.
3. **Live TCP/SSE E2E Smoke Suite (`scripts/smoke_e2e.py`)**: memverifikasi server `uvicorn` hidup (UI `/`, `/api/health`, 3 skenario `SAT -> PATCH -> UNSAT`, `HOOK_AUDIT`, `PROXY_AUDIT`).
4. **LightVela VPS Staging & Offline Demo Scripts**: `scripts/vps-stage.sh`, `scripts/vps-tunnel.sh` (`--protocol http2`), `scripts/demo-offline.sh`, `deploy/proofforge-api.service`, dan `docs/PREFLIGHT-CHECKLIST-NYC.md`.

## Cara Menerapkan

```bash
cd ~/projects/proofforge-3d
git fetch origin
git checkout feat/pf-005-phase1
git pull --ff-only origin feat/pf-005-phase1

unzip -o /path/to/proofforge-phase2-staging-overlay.zip -d .

# Re-install editable package setelah perbaikan pyproject.toml & jalankan full gate + live smoke
bash scripts/vps-stage.sh
```

Setelah `SMOKE_E2E_OK` dan `VERIFY_OK`, merge `feat/pf-005-phase1` ke `main`!
