# HANDOFF.md — State Estafet Lintas Agen

File ini **WAJIB** dibaca di awal sesi dan diperbarui di akhir sesi oleh setiap agen (**Arena.ai**, **Hermes Agent @ LightVela VPS**, **OpenCode**).

---

## Status Terkini

* **Active Phase:** Phase 1 — Scaffold Non-AI & Mesin Deterministik Z3 + 3D
* **Last Updated:** 2026-11-17 (Arena.ai via Overlay Package)
* **Last Actor:** Arena.ai
* **Repo Target:** `https://github.com/Niumination/proofforge-3d` — synced @ `423388e` + Phase 1 unlock
* **Active Task:** `PF-005` s.d. `PF-008` (Batch 1A — pelaksana OpenCode di branch `feat/pf-005-core-scaffold`)
* **Code Lock Status:** **PHASE_1_UNLOCKED** — Diizinkan menulis scaffold non-AI, FastAPI SSE, Z3 runner deterministik, skenario Z3+3D, dan Cockpit UI (dilarang menulis integrasi Gemini 4 / Managed Agents sebelum Phase 3 hari-H).

---

## Apa yang Sudah Selesai

- [x] Visi, positioning hadiah ($7,500 Main + $5,000 Best Use of Managed Agents), dan pendaftaran Cerebral Valley terkunci.
- [x] Dokumen arsitektur inti (`README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `BACKLOG.md`).
- [x] Dokumen brainstorming skenario 3D, scaffold blueprint, workflow 4-platform, naskah pitch 2 menit, dan `docs/Z3-SCENARIO-MATH-SPECS.md`.
- [x] Repo GitHub live (`PF-003`) & LightVela VPS terverifikasi (`PF-004`).

---

## Langkah Selanjutnya (Next Action)

1. **OpenCode (Batch 1A — `PF-005` s.d. `PF-008`):** Buat branch `feat/pf-005-core-scaffold`, bangun struktur monorepo (`apps/web`, `apps/api`, `sandbox-agent`, `scenarios`, `scripts/verify.sh`), `.env.example`, GitHub Actions CI, FastAPI + SSE stream, serta `invariant_guard.py` + `z3_runner.py` (mode `deterministic`).
2. **OpenCode + Arena.ai (Batch 1B — `PF-009` s.d. `PF-011`):** Implementasikan 3 skenario (`drone_swarm`, `robot_arm`, `spatial_tiling`) mengacu pada `docs/Z3-SCENARIO-MATH-SPECS.md` revisi terbaru.
3. **OpenCode (Batch 1C — `PF-012` s.d. `PF-014`):** Bangun 3-pane Cockpit UI + Three.js 3D Viewport + Time Scrubber + Audit Hooks/Proxy Panel.
4. **Hermes Agent @ LightVela VPS (`PF-015`):** Pull perubahan Phase 1, jalankan `bash scripts/verify.sh` di Linux bersih, dan update hasil ke `HANDOFF.md`.

---

## Catatan Handoff Terbaru

```text
[2026-11-17 | Arena.ai]
- What Changed:
  1. Code Lock Status dibuka menjadi PHASE_1_UNLOCKED untuk memulai Batch 1A (PF-005..PF-008).
  2. Revisi penyempurnaan di docs/Z3-SCENARIO-MATH-SPECS.md:
     - Scenario A (drone_swarm): gunakan bentuk kuadratik `dx² + dy² >= R_safe²` di Z3 (tanpa sqrt) dan lintasan head-on berlawanan arah (gap awal 118.86m → 0.38m pada t=4.2s) agar efek 3D dramatis & stopping-distance 85.5m selalu muat.
     - Scenario B (robot_arm): pastikan linearisasi Taylor juga diterapkan pada `y_effector >= 0.15m` agar seluruh model tetap QF_LIA murni.
     - Scenario C (spatial_tiling): spawn W1 & W2 di sudut berjauhan pada grid 4x4x4 sehingga konvergensi & circular wait >= 4 tick terjadi tepat sekitar tick 14..18 (DEADLOCK DETECTED at tick 18).
- Next Task ID: PF-005..PF-008 (OpenCode, branch feat/pf-005-core-scaffold).
- Blockers: none.
```

```text
[2026-11-17 | Hermes Agent @ LightVela VPS]
- What Changed: repo di-clone ke ~/projects/proofforge-3d (terisolasi dari OMB/9Router — folder terpisah, service produksi tidak disentuh); PF-003 & PF-004 ditandai [x] di BACKLOG.md; Active Task → PF-005.
- VPS Readiness (bukti perintah dijalankan):
  - git --version          → git version 2.43.0
  - python3 --version      → Python 3.11.16        (target >= 3.11 ✓)
  - node -v                → v22.23.4              (target >= 20 ✓)
  - pnpm -v                → 10.33.0               ✓
  - cloudflared --version  → 2026.10.0             ✓ (siap staging tunnel --protocol http2)
  - git pull --ff-only origin main → "Already up to date" @ 1c07519 (sinkronisasi OK)
- Tests Passed: verifikasi struktur 11 file Phase 0 lengkap (root 6 + docs/ 5).
- Next Task ID: PF-005 (OpenCode, branch feat/pf-005-core-scaffold) — menunggu Code Lock → PHASE_1_UNLOCKED dari user.
- Blockers: tidak ada teknis; hanya menunggu keputusan unlock Phase 1.
- Catatan Arena.ai dipatuhi: folder terpisah dari runtime OpenMausBot/9Router; skema ARCHITECTURE.md tidak diubah.
```
