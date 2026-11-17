# BACKLOG.md — Peta Kerja ProofForge 3D

Pelacakan tugas lintas agen (**Arena.ai**, **Hermes Agent @ LightVela VPS**, **OpenCode**, dan **Eksekusi Hari-H Hackathon**).

**Aturan Status:**
* `[ ]` Belum dikerjakan
* `[~]` Sedang dikerjakan (tulis nama agen di kolom Owner & catat di `HANDOFF.md`)
* `[x]` Selesai & terverifikasi dengan bukti perintah uji

---

## Phase 0 — Dokumentasi, Arsitektur & Setup Repo (Target: 17 Nov 2026)

| ID | Tugas | Owner | Output / File | Status |
| :--- | :--- | :--- | :--- | :--- |
| `PF-001` | Finalisasi dokumen visi, kontrak agen, dan arsitektur teknis | Arena.ai | `README.md`, `AGENTS.md`, `ARCHITECTURE.md` | `[x]` |
| `PF-002` | Susun brainstorming skenario 3D, scaffold blueprint, workflow multi-agen, dan naskah pitch | Arena.ai | `docs/*.md`, `BACKLOG.md`, `HANDOFF.md` | `[x]` |
| `PF-003` | Buat repo GitHub baru `Niumination/proofforge-3d` & push dokumentasi Phase 0 | Human + Hermes | GitHub repo live & terindeks | `[x]` Repo live @ `1c07519`, 11 file terverifikasi via clone VPS |
| `PF-004` | Setup workspace terisolasi di VPS LightVela & uji sinkronisasi Hermes Agent | Hermes (LightVela) | Clone repo + konfirmasi `HANDOFF.md` | `[x]` Clone `~/projects/proofforge-3d` (isolasi dari OMB/9Router), toolchain diverifikasi — bukti di `HANDOFF.md` |

---

## Phase 1 — Scaffold Non-AI & Mesin Deterministik Z3 + 3D (Target: 18–19 Nov 2026)

> *Catatan Kepatuhan Hackathon: Fase ini hanya membangun kerangka aplikasi umum, visualizer 3D, dan verifier Z3 lokal yang deterministik—belum menulis logika integrasi AI inti Gemini 4.*

| ID | Tugas | Owner | Output / File | Status |
| :--- | :--- | :--- | :--- | :--- |
| `PF-005` | Inisialisasi monorepo scaffold (`apps/web`, `apps/api`, `sandbox-agent`, `scenarios`, `scripts`) | OpenCode | Struktur direktori & config build bersih | `[ ]` |
| `PF-006` | Setup `.env.example`, `.gitignore`, dan GitHub Actions CI (typecheck + pytest + secret scan) | OpenCode + Hermes | `.github/workflows/ci.yml`, `.env.example` | `[ ]` |
| `PF-007` | Bangun backend FastAPI dasar + endpoint `/api/health` & `/api/forge/stream/{run_id}` (SSE) | OpenCode | `apps/api/main.py`, `apps/api/stream.py` | `[ ]` |
| `PF-008` | Implementasi engine runner Z3 lokal + pengunci SHA-256 `invariants_locked.py` | OpenCode | `apps/api/verifier/z3_runner.py` | `[ ]` |
| `PF-009` | Implementasi **Skenario A (Drone Swarm Collision Avoidance)** beserta bug awal & trace 3D | OpenCode + Arena | `scenarios/drone_swarm/` | `[ ]` |
| `PF-010` | Implementasi **Skenario B (Robot Arm Torque & Joint Envelope)** | OpenCode + Arena | `scenarios/robot_arm/` | `[ ]` |
| `PF-011` | Implementasi **Skenario C (Spatial Tiling Deadlock)** | OpenCode + Arena | `scenarios/spatial_tiling/` | `[ ]` |
| `PF-012` | Bangun Frontend Cockpit UI: 3-pane layout (Spec Ledger, 3D Viewport, Proof/Security Audit) | OpenCode | `apps/web/src/App.tsx`, store Zustand | `[ ]` |
| `PF-013` | Bangun Three.js 3D State-Space Viewport + Time Scrubber + Red Collision/Breach Highlight | OpenCode | `apps/web/src/components/Viewport3D.tsx` | `[ ]` |
| `PF-014` | Bangun Panel Diff Patch & Panel Audit Hooks/Proxy (simulasi event SSE lokal) | OpenCode | `apps/web/src/components/AuditPanel.tsx` | `[ ]` |
| `PF-015` | Verifikasi E2E Phase 1 via `scripts/verify.sh` di lokal & LightVela VPS | Hermes (LightVela) | Laporan lulus 0 error di `HANDOFF.md` | `[ ]` |

---

## Phase 2 — Pre-Flight Staging & Kesiapan Demo NYC (Target: 20 Nov 2026)

| ID | Tugas | Owner | Output / File | Status |
| :--- | :--- | :--- | :--- | :--- |
| `PF-016` | Deploy staging demo deterministik di LightVela VPS (atau pastikan jalan 100% offline/lokal di laptop demo) | Hermes (LightVela) | Tunnel `--protocol http2` / offline script | `[ ]` |
| `PF-017` | Siapkan `.agents/skills/` & template `AGENTS.md`/`SKILL.md` untuk Antigravity Managed Agent | Arena + OpenCode | `sandbox-agent/AGENTS.md`, `SKILL.md` | `[ ]` |
| `PF-018` | Uji coba kering (dry run) alur pitch 2 menit dengan mode fallback deterministik | Human + Arena | Checklist kesiapan laptop & browser | `[ ]` |

---

## Phase 3 — Live Hackathon Build (Sabtu, 21 Nov 2026 · 09:00–22:00 EST · NYC)

| ID | Tugas | Waktu Target (EST) | Output / Fokus | Status |
| :--- | :--- | :--- | :--- | :--- |
| `PF-019` | Registrasi venue, klaim kredit API Google DeepMind, verifikasi akses `gemini-4-argon` & `antigravity-preview-09-2026` | 09:00 – 09:45 | `.env` lokal terisi & smoke test API sukses | `[ ]` |
| `PF-020` | Integrasi `gemini-4-argon` Co-Generator (Spec → Code + Z3 Harness + 3D Adapter JSON) | 09:45 – 12:00 | `apps/api/agents/argon_synth.py` | `[ ]` |
| `PF-021` | Integrasi `antigravity-preview-09-2026` Managed Agents (remote Linux sandbox runner) | 12:00 – 14:30 | `apps/api/agents/managed_runner.py` | `[ ]` |
| `PF-022` | Implementasi **Protected Hooks** (blokir modifikasi `invariants_locked.py` + scope guard) | 14:30 – 16:00 | Hook aktif & terbukti memblokir test tamper | `[ ]` |
| `PF-023` | Implementasi **Credential Proxy** (ekspor Proof Certificate / GitHub PR terverifikasi tanpa ekspos token) | 16:00 – 17:15 | `PROXY_AUDIT` live di UI | `[ ]` |
| `PF-024` | Implementasi Closed-Loop Self-Patching (`SAT` → `argon` patch → re-verify → `UNSAT`) | 17:15 – 18:30 | Minimal 3 skenario sukses `SAT -> UNSAT` | `[ ]` |
| `PF-025` | *(Stretch)* Tambah button **"Simulate Prompt Injection Attack"** untuk demo Protected Hook & Proxy | 18:30 – 19:15 | Tombol Red-Team live di UI | `[ ]` |
| `PF-026` | *(Stretch)* Integrasi Voice Input via `gemini-3.8-live` untuk modifikasi constraint langsung | 19:15 – 19:45 | Voice-to-constraint bekerja | `[ ]` |
| `PF-027` | Freeze fitur, full E2E test, dan siapkan mode fallback aman bila Wi-Fi venue padat | 19:45 – 20:30 | Build stabil siap panggung | `[ ]` |
| `PF-028` | Rekam video demo cadangan & submit proyek ke portal hackathon Cerebral Valley | 20:30 – 21:15 | Submission terkirim sebelum deadline | `[ ]` |
| `PF-029` | Judging & Pitch Live 2 Menit di depan tim Google DeepMind | 21:15 – 22:00 | Demo sukses | `[ ]` |
