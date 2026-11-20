# HANDOFF.md — State Estafet Lintas Agen

File ini **WAJIB** dibaca di awal sesi dan diperbarui di akhir sesi oleh setiap agen (**Arena.ai**, **Hermes Agent @ LightVela VPS**, **OpenCode**).

---

## Status Terkini

* **Active Phase:** Phase 1 — Scaffold Non-AI & Mesin Deterministik Z3 + 3D
* **Last Updated:** 2026-11-20 (Arena.ai Phase 1 Overlay Build)
* **Last Actor:** Arena.ai
* **Repo Target:** `https://github.com/Niumination/proofforge-3d`
* **Active Task:** `PF-015` — Verifikasi E2E Phase 1 via `scripts/verify.sh` oleh Hermes Agent @ LightVela VPS
* **Code Lock Status:** **PHASE_1_UNLOCKED** — Phase 1 Non-AI Core + Z3 Scenarios + Cockpit UI lengkap dan terverifikasi (`pytest`, `ruff`, `tsc`, `vite build`, `vitest`). Phase 3 AI integrations (`gemini-4-argon`, `antigravity-preview-09-2026`) tetap dikunci hingga Hackathon Day (Nov 21, 2026).

---

## Apa yang Sudah Selesai

- [x] Phase 0 dokumentasi & blueprint (`PF-001`–`PF-004`).
- [x] Monorepo scaffold, `.env.example`, `.github/workflows/ci.yml`, `scripts/verify.sh` (`PF-005`–`PF-006`).
- [x] Backend FastAPI SSE orchestrator + SHA-256 `invariant_guard.py` + real `z3-solver` runner (`PF-007`–`PF-008`).
- [x] Tiga skenario Z3 + 3D real (`drone_swarm` 101 frames, `robot_arm` 41 frames, `spatial_tiling` 25 frames) sesuai `docs/Z3-SCENARIO-MATH-SPECS.md` (`PF-009`–`PF-011`).
- [x] Frontend 3-pane Cockpit UI + Three.js Viewport + Time Scrubber + Patch Diff Modal + Hooks/Proxy Audit Panel (`PF-012`–`PF-014`).
- [x] `sandbox-agent/` & `.agents/skills/` templates (`PF-017`).

---

## Langkah Selanjutnya (Next Action)

1. **OpenCode:** Terapkan Phase 1 overlay ke branch `feat/pf-005-phase1`, jalankan `bash scripts/verify.sh`, lalu merge ke `main` setelah lolos.
2. **Hermes Agent @ LightVela VPS (`PF-015`):** `git pull` repo terbaru, jalankan `bash scripts/verify.sh` di Linux bersih, dan uji smoke test API + UI staging (`PF-016`).

---

## Catatan Handoff Terbaru

```text
[2026-11-20 | Arena.ai]
- What Changed:
  1. Diaudit branch `feat/pf-005-phase1` (`41c35a6`) dan disiapkan Phase 1 Replacement Overlay yang teruji penuh:
     - Perbaikan seluruh bug pada `forge.py`, `z3_runner.py`, `deterministic_sim.py`, `sseClient.ts`, `apiClient.ts`, `forgeStore.ts`, `Viewport3D.tsx`, `TimeScrubber.tsx`, `SpecPanel.tsx`, `AuditPanel.tsx`, dan `PatchDiffModal.tsx`.
     - Implementasi Z3 SMT nyata (`z3-solver`) untuk `drone_swarm` (quadratic separation SAT -> UNSAT), `robot_arm` (QF_LIA Taylor torque + table height SAT -> UNSAT), dan `spatial_tiling` (corner-spawn tick-18 deadlock SAT -> UNSAT).
     - Pembuatan `apps/api/tests/test_phase1.py` (5 test) + `apps/web/src/App.test.tsx` (2 test).
- Tests Passed (Arena Sandbox):
  - `pytest apps/api -v` → 5 passed
  - `ruff check apps/api scenarios sandbox-agent` → All checks passed (0 errors)
  - `tsc -b --noEmit` → 0 errors
  - `vite build` → dist/ built cleanly
  - `vitest run` → 2 passed
- Next Task ID: PF-015 (Hermes Agent @ LightVela VPS).
- Blockers: none.
```
