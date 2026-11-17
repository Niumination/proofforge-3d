# Scaffold Blueprint & Kebutuhan Teknis — ProofForge 3D

Dokumen ini menjabarkan **struktur file dan folder lengkap** yang akan dibangun mulai Phase 1, beserta daftar dependensi dan kontrak konfigurasi.  
*(Belum ada kode aplikasi yang dibuat pada Phase 0).*

---

## 1. Pohon Direktori Lengkap (Target Monorepo)

```text
proofforge-3d/
├── README.md                          # Ringkasan proyek, tesis, & peta dokumen
├── AGENTS.md                          # Kontrak mutlak lintas agen (Arena, Hermes, OpenCode, Gemini)
├── ARCHITECTURE.md                    # Arsitektur 4-lapis, alur closed-loop, kontrak JSON/SSE
├── BACKLOG.md                         # Task tracker PF-001 s.d. PF-029
├── HANDOFF.md                         # State estafet hidup antar agen
├── .gitignore                         # Isolasi secrets, venv, node_modules, runtime artifacts
├── .env.example                       # Template variabel lingkungan (tanpa nilai rahasia)
├── opencode.json                      # Konfigurasi OpenCode untuk workspace lokal
│
├── .github/
│   └── workflows/
│       └── ci.yml                     # CI: TS typecheck, Vitest, Pytest, Z3 smoke test, secret scan
│
├── .agents/
│   └── skills/                        # Skill terkurasi proyek (pola MIRAI / ecosystem-config)
│       ├── z3-formal-modeling/
│       │   └── SKILL.md               # Aturan pemodelan Z3 cepat & anti-timeout
│       ├── threejs-counterexample-ui/
│       │   └── SKILL.md               # Konvensi visualisasi frame merah & time scrubber
│       └── managed-agents-hooks/
│           └── SKILL.md               # Konvensi Protected Hooks & Credential Proxy
│
├── docs/
│   ├── BRAINSTORMING-AND-DEMO-SCENARIOS.md
│   ├── SCAFFOLD-BLUEPRINT.md
│   ├── MULTI-AGENT-WORKFLOW.md
│   ├── HACKATHON-PITCH-AND-JUDGING.md
│   └── GITHUB-SETUP.md
│
├── apps/
│   ├── web/                           # Frontend Cockpit (Vite 7 + React 19 + TS + Tailwind v4)
│   │   ├── package.json
│   │   ├── tsconfig.json
│   │   ├── vite.config.ts
│   │   ├── index.html
│   │   └── src/
│   │       ├── main.tsx
│   │       ├── App.tsx                # Layout 3-pane + Header Mode Switch + Demo Presets
│   │       ├── App.css                # Tailwind v4 @theme (high-contrast dark cockpit)
│   │       ├── types/
│   │       │   └── forge.ts           # Kontrak TypeScript (mirror ARCHITECTURE.md §4)
│   │       ├── store/
│   │       │   ├── forgeStore.ts      # Zustand: run state, iteration history, playback tick
│   │       │   └── auditStore.ts      # Zustand: SSE logs, hook blocks, proxy audit events
│   │       ├── lib/
│   │       │   ├── sseClient.ts       # Koneksi EventSource / fetch stream ke FastAPI
│   │       │   └── apiClient.ts       # Wrapper REST API (/api/forge/run, /api/export)
│   │       └── components/
│   │           ├── SpecPanel.tsx      # Pane kiri: pilih skenario, lock invarian, red-team toggle
│   │           ├── Viewport3D.tsx     # Pane tengah: Three.js/R3F canvas + kamera + safety spheres
│   │           ├── TimeScrubber.tsx   # Kontrol play/pause, lompat ke violated_tick, Before/After
│   │           ├── AuditPanel.tsx     # Pane kanan: Z3 SAT/UNSAT badge, Hooks Log, Proxy Log
│   │           └── PatchDiffModal.tsx # Penampil unified diff per iterasi
│   │
│   └── api/                           # Backend Orchestrator (Python 3.11+ + FastAPI)
│       ├── pyproject.toml             # Dependensi & konfigurasi pytest/ruff
│       ├── main.py                    # Entrypoint FastAPI + CORS + static/health
│       ├── config.py                  # Loader env & mode flag (live vs fallback)
│       ├── models/
│       │   └── schemas.py             # Pydantic models sesuai ARCHITECTURE.md §4
│       ├── routes/
│       │   ├── forge.py               # POST /api/forge/run, GET /api/forge/stream/{id}
│       │   └── export.py              # POST /api/forge/export (lewat Credential Proxy)
│       ├── verifier/
│       │   ├── invariant_guard.py     # SHA-256 lock & verifikasi anti-tampering
│       │   ├── z3_runner.py           # Runner subprocess Z3 dengan timeout & parser trace
│       │   └── scene_exporter.py      # Konversi hasil simulasi ke SceneTimelineFrame[]
│       └── agents/
│           ├── interface.py           # Abstraksi AgentRunner (memisahkan Phase 1 & Phase 3)
│           ├── deterministic_sim.py   # Simulator lokal Phase 1 (tanpa API AI eksternal)
│           ├── argon_synth.py         # [Phase 3] Gemini 4 Argon co-generator & patcher
│           └── managed_runner.py      # [Phase 3] Google Managed Agents (antigravity) client
│
├── sandbox-agent/                     # Paket definisi untuk Google Managed Agents sandbox
│   ├── AGENTS.md                      # Instruksi agen di dalam sandbox Linux Google
│   ├── SKILL.md                       # Skill eksekusi Z3 & aturan surgical patch
│   └── hooks/
│       ├── pre_verify_guard.py        # Cek SHA-256 invariants_locked.py sebelum Z3 jalan
│       └── write_scope_guard.py       # Tolak penulisan di luar workspace/impl/
│
├── scenarios/                         # 3 Skenario Flagship siap jalan & terisolasi
│   ├── drone_swarm/
│   │   ├── spec.md                    # Deskripsi masalah & metrik untuk Gemini 4 Argon
│   │   ├── invariants_locked.py       # Kontrak Z3 terkunci (read-only + hash)
│   │   ├── buggy_impl.py              # Implementasi awal dengan bug stopping-distance
│   │   └── scene_adapter.py           # Pembuat koordinat 3D quadrotor & safety sphere
│   ├── robot_arm/
│   │   ├── spec.md
│   │   ├── invariants_locked.py
│   │   ├── buggy_impl.py
│   │   └── scene_adapter.py
│   └── spatial_tiling/
│       ├── spec.md
│       ├── invariants_locked.py
│       ├── buggy_impl.py
│       └── scene_adapter.py
│
└── scripts/
    ├── verify.sh                      # Satu perintah verifikasi total (typecheck + pytest + Z3)
    ├── dev-local.sh                   # Jalankan api (:8000) + web (:5173) bersamaan
    └── pre-event-check.sh             # Cek kesiapan Z3, Node, Python, & konektivitas API
```

---

## 2. Daftar Kebutuhan Perangkat Lunak (Bill of Materials)

### 2.1 Lingkungan Sistem (Lokal & LightVela VPS)
* **Node.js:** `>= 20` (atau v24/v26 sesuai lingkungan `Niumination`) + `pnpm`
* **Python:** `>= 3.11` dengan `uv` atau `venv`
* **Git + GitHub CLI (`gh`)** untuk pelacakan & automasi repo
* **Cloudflared** *(opsional di LightVela VPS)* dengan `--protocol http2` untuk staging URL

### 2.2 Dependensi Frontend (`apps/web`)
* `react` & `react-dom` (`^19.x`)
* `three`, `@types/three`, `@react-three/fiber`, `@react-three/drei` (rendering 3D WebGL)
* `zustand` (`^5.x`) untuk state manajemen timeline & telemetry
* `lucide-react` untuk ikon konsol keamanan/audit
* `tailwindcss` (`^4.x`) + `@tailwindcss/vite`
* Dev/Test: `typescript`, `vite`, `vitest`, `@testing-library/react`

### 2.3 Dependensi Backend (`apps/api`)
* `fastapi` + `uvicorn[standard]` + `sse-starlette` (API + SSE streaming)
* `pydantic` (`>= 2.x`)
* `z3-solver` (Microsoft Z3 SMT solver Python bindings)
* `google-genai` *(diaktifkan pada Phase 3 untuk Interactions API, `gemini-4-argon`, dan `antigravity-preview-09-2026`)*
* Dev/Test: `pytest`, `httpx`, `ruff`

---

## 3. Kontrak Variabel Lingkungan (`.env.example`)

Semua rahasia **tidak boleh** masuk Git. Pada Phase 1, file `.env.example` dibuat dengan struktur berikut:

```ini
# Mode Operasi: "deterministic" (Phase 1-2) atau "live_gemini" (Phase 3 Hari-H)
PROOFFORGE_MODE=deterministic

# Server Ports (selaras dengan reverse-proxy/tunnel)
API_HOST=127.0.0.1
API_PORT=8000
VITE_API_BASE_URL=/api

# Kredensial Google DeepMind (diisi saat venue hackathon Nov 21, 2026)
GEMINI_API_KEY=
GEMINI_FRONTIER_MODEL=gemini-4-argon
GEMINI_FAST_MODEL=gemini-3.8-flash
GEMINI_MANAGED_AGENT_ID=antigravity-preview-09-2026

# Credential Proxy Target (untuk demo ekspor Proof Certificate tanpa ekspos token)
MANAGED_PROXY_GITHUB_CREDENTIAL_REF=
GITHUB_EXPORT_REPO=Niumination/proofforge-3d-proofs
```

---

## 4. Kebutuhan Non-Fungsional (Kriteria Kualitas)

1. **Zero-Error Gate (`scripts/verify.sh`):**
   * `tsc --noEmit` harus exit `0`.
   * `pytest` (termasuk tes Z3 untuk ketiga skenario *buggy = SAT* dan *fixed = UNSAT*) harus exit `0`.
   * `ruff check` bersih tanpa error.
2. **Latensi Demo:**
   * Mode lokal/deterministik: `< 1.5 detik` dari klik *Run* hingga animasi 3D muncul.
   * Mode live Gemini 4 + Managed Agents: target `< 25–35 detik` end-to-end (dengan streaming SSE setiap langkah agar layar tidak pernah terlihat membeku).
3. **Browser-Safe Proxy:** Frontend hanya memanggil relative URL `/api/...` (melalui Vite dev proxy saat pengembangan, atau FastAPI/reverse proxy saat produksi) — **tidak pernah** hardcode `localhost` di kode browser agar bisa langsung di-preview lewat tunnel apa pun.
