# BACKLOG.md — Peta Kerja ProofForge 3D

Pelacakan tugas lintas agen (**Arena.ai**, **Hermes Agent @ LightVela VPS**, **OpenCode**, dan **Eksekusi Hari-H Hackathon**).

**Aturan Status:**
* `[ ]` Belum dikerjakan
* `[~]` Sedang dikerjakan (tulis nama agen di kolom Owner & catat di `HANDOFF.md`)
* `[x]` Selesai & terverifikasi dengan bukti perintah uji

---

## Phase 0 – Phase 2 (Selesai & Ter-merge ke `main` @ `c72e03f`)

| ID | Tugas | Owner | Output / File | Status |
| :--- | :--- | :--- | :--- | :--- |
| `PF-001`–`PF-004` | Dokumentasi Phase 0, repo GitHub, LightVela VPS isolation | Arena + Hermes | `README.md`, `AGENTS.md`, `ARCHITECTURE.md` | `[x]` |
| `PF-005`–`PF-014` | Monorepo scaffold, FastAPI SSE, Z3 3 skenario, Cockpit UI | OpenCode + Arena | `apps/*`, `scenarios/*` | `[x]` |
| `PF-015`–`PF-018` | Single-process SPA serving, live `smoke_e2e.py`, VPS scripts, dry-run kit | Arena + Hermes | `scripts/*`, `deploy/*`, `docs/PREFLIGHT-CHECKLIST-NYC.md` | `[x]` |

---

## Phase 3 — Live Hackathon Build (`pkg1`..`pkg7`)

| ID | Tugas | Paket | Output / Fokus | Status |
| :--- | :--- | :--- | :--- | :--- |
| `PF-019` | Preflight script `scripts/preflight_gemini.py` (isi `.env` live di venue) | Pkg 1 | `scripts/preflight_gemini.py` | `[x]` |
| `PF-020` | `gemini-4-argon` Co-Generator + AST guard + `dynamic_runner.py` | Pkg 1+6 | `apps/api/agents/argon_synth.py`, `verifier/dynamic_runner.py` | `[x]` |
| `PF-021` | `antigravity-preview-09-2026` Managed Agents + local subprocess parity | Pkg 2 | `apps/api/agents/managed_runner.py` | `[x]` |
| `PF-022` | **Protected Hooks** (SHA-256 tamper block, write scope, prompt-injection & secret scrubber) | Pkg 2 | `apps/api/security/protected_hooks.py` | `[x]` |
| `PF-023` | **Credential Proxy** + Signed Proof Certificate JSON (`/api/forge/certificate/{id}`) | Pkg 2 | `apps/api/security/credential_proxy.py`, `routes/export.py` | `[x]` |
| `PF-024` | Closed-Loop Self-Patching (`SAT -> PATCH -> UNSAT` + fallback deterministik) | Pkg 3+6 | `apps/api/agents/closed_loop.py`, `routes/forge.py` | `[x]` |
| `PF-025` | Red-Team **Simulate Prompt Injection Attack** API + tombol UI | Pkg 3+4 | `/api/forge/redteam`, `SpecPanel.tsx` | `[x]` |
| `PF-026` | Voice-to-Constraint API (`gemini-3.8-flash` + fallback) + Web Speech & 1-click presets | Pkg 3–6 | `/api/forge/voice-constraint`, `SpecPanel.tsx` | `[x]` |
| `PF-027` | Full build freeze + `verify.sh` + live `smoke_e2e.py` + `jsdom` React UI mount test + judge docs | Pkg 4–7 | `apps/web/src/App.test.tsx`, `docs/PITCH-QUICK-CARD.md`, `README.md` | `[x]` |
| `PF-028` | Rekam video cadangan 120 detik & submit ke portal Cerebral Valley | Human | Submission Hari-H NYC | `[ ]` |
| `PF-029` | Judging & Live 2-Minute Pitch di depan tim Google DeepMind | Human | Presentasi panggung NYC | `[ ]` |
