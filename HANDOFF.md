# HANDOFF.md — State Estafet Lintas Agen

File ini **WAJIB** dibaca di awal sesi dan diperbarui di akhir sesi oleh setiap agen (**Arena.ai**, **Hermes Agent @ LightVela VPS**, **OpenCode**).

---

## Status Terkini

* **Active Phase:** Phase 2 — Pre-Flight Staging & Kesiapan Demo NYC (`PF-015`..`PF-018`)
* **Last Updated:** 2026-11-20 (Arena.ai Phase 2 Staging Overlay)
* **Last Actor:** Arena.ai
* **Repo Target:** `https://github.com/Niumination/proofforge-3d`
* **Active Task:** `PF-015` & `PF-016` — Hermes Agent @ LightVela VPS menjalankan `bash scripts/vps-stage.sh` + merge `feat/pf-005-phase1` → `main`
* **Code Lock Status:** **PHASE_2_STAGING** — Single-process production UI+API serving, live TCP/SSE smoke suite, LightVela VPS staging scripts, dan naskah dry-run 120 detik selesai. Integrasi AI Phase 3 (`gemini-4-argon`, `antigravity-preview-09-2026`) tetap dikunci hingga Hackathon Day (Nov 21, 2026).

---

## Apa yang Sudah Selesai

- [x] Phase 0 dokumentasi & blueprint (`PF-001`–`PF-004`).
- [x] Phase 1 Non-AI Core + Real Z3 Scenarios + Three.js 3D Cockpit (`PF-005`–`PF-014`, `PF-017`) ter-push ke `feat/pf-005-phase1` (`f5fb2a2`).
- [x] Perbaikan packaging `apps/api/pyproject.toml` (`[tool.setuptools.packages.find]`) sehingga `pip install -e "./apps/api[dev]"` berjalan bersih tanpa error flat-layout.
- [x] Single-process production SPA serving di `apps/api/main.py` (`apps/web/dist` + path-traversal guard + `/api/*` isolation).
- [x] Live TCP/HTTP/SSE smoke test (`scripts/smoke_e2e.py`) mencakup `/`, `/api/health`, dan alur penuh 3 skenario + proxy export.
- [x] Skrip VPS staging & tunnel (`scripts/vps-stage.sh`, `scripts/vps-tunnel.sh`, `scripts/demo-offline.sh`, `deploy/proofforge-api.service`) + `docs/PREFLIGHT-CHECKLIST-NYC.md`.

---

## Langkah Selanjutnya (Next Action)

1. **OpenCode / Human:** Ekstrak `proofforge-phase2-staging-overlay.zip` di branch `feat/pf-005-phase1`, jalankan `bash scripts/verify.sh`, commit + push, lalu merge `feat/pf-005-phase1` → `main`.
2. **Hermes Agent @ LightVela VPS (`PF-015` & `PF-016`):** Jalankan `bash scripts/vps-stage.sh` di `~/projects/proofforge-3d`, tandai `PF-015`/`PF-016` `[x]`, dan uji `scripts/vps-tunnel.sh` bila perlu staging publik.
3. **Human (`PF-018`):** Lakukan 1× dry run 120 detik mengikuti `docs/PREFLIGHT-CHECKLIST-NYC.md` di `http://127.0.0.1:8000`.

---

## Catatan Handoff Terbaru

```text
[2026-11-20 | Arena.ai]
- What Changed (Phase 2 Staging Overlay):
  1. Memperbaiki `apps/api/pyproject.toml` (`[tool.setuptools.packages.find]`) agar `pip install -e "./apps/api[dev]"` tidak gagal flat-layout discovery.
  2. Menambahkan SPA static serving (`apps/web/dist`) di `apps/api/main.py` + `apps/api/config.py` untuk mode offline 1-proses & tunnel VPS.
  3. Menambahkan `scripts/smoke_e2e.py` (uji live TCP/HTTP/SSE untuk 3 skenario + static SPA) dan test unit baru di `apps/api/tests/test_phase1.py`.
  4. Menambahkan `scripts/demo-offline.sh`, `scripts/vps-stage.sh`, `scripts/vps-tunnel.sh`, `deploy/proofforge-api.service`, dan `docs/PREFLIGHT-CHECKLIST-NYC.md`.
- Tests Passed (Arena Sandbox):
  - `pip install -e "./apps/api[dev]"` → clean editable install
  - `bash scripts/verify.sh` → tsc, vite build, vitest (2), ruff, pytest (6) ALL PASS
  - Live `uvicorn` + `scripts/smoke_e2e.py --require-ui` → SMOKE_E2E_OK (all 3 scenarios + UI)
- Next Task ID: PF-015 & PF-016 (Hermes Agent @ LightVela VPS) + merge feat/pf-005-phase1 -> main.
- Blockers: none.
```
