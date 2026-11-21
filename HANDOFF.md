# ProofForge 3D — Engineering & Pitch Handoff

## Current Status
**Phase 1–5 Complete & Verified (`pkg1`–`pkg13`).**
- **Test Suites:** `24/24` backend pytest tests passing, `3/3` frontend Vitest (`jsdom` + React 19 mount + `1-Click Stage Auto-Demo` + modal Copy/Report buttons) passing, `ruff check` + `tsc --noEmit` + `vite build` clean.
- **Live E2E Smoke:** `/api/health` (readiness metadata), `/api/forge/scenarios`, `/api/forge/run`, `/api/forge/stream/{run_id}`, `/api/forge/export`, `/api/forge/certificate/{cert_id}`, `/api/forge/report/{cert_id}`, parametric `r_safe_m=2.2m` Z3 telemetry, `/api/forge/redteam`, and `/api/forge/voice-constraint` all verified against live Uvicorn + built SPA.

## Stage Keyboard Controls
- `Space`: Play / Pause 3D simulation
- `F`: Focus violation frame
- `B`: Toggle `BEFORE · BUG (SAT)` ↔ `AFTER · PATCHED (UNSAT)`
- `Esc`: Close open Diff / Certificate modals

## Remaining Human Actions
- **PF-028:** Record 2-minute demo video & submit final portal form (`docs/SUBMISSION-PORTAL-KIT.md`). — **Done** (user: "aku sudah rekam semuanya"; portal submission flow ditandai selesai).
- **PF-029:** Rehearse 3-minute live pitch (`docs/PITCH-QUICK-CARD.md`).
