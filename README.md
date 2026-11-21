# ProofForge 3D

> **Self-Verifying Systems Compiler & 3D Visual Counterexample Engine**  
> Built for **Gemini 4 NYC Hackathon** (Cerebral Valley × Google DeepMind — Nov 21, 2026)

[![Target Event](https://img.shields.io/badge/Event-Gemini%204%20NYC%20Hackathon-4285F4)](#)
[![Track](https://img.shields.io/badge/Tracks-Advanced%20Reasoning%20%7C%20Visual%20Coding%20%7C%20Managed%20Agents-34A853)](#)
[![Status](https://img.shields.io/badge/Build-Verified%20Phase%201--3%20Ready-00C853)](#)

---

## 1. Visi & Arsitektur Closed-Loop

AI coding agents write code that compiles and looks right—until edge-case physics, actuator torque limits, or concurrency deadlocks fail catastrophically. **ProofForge 3D** closes that gap:

1. **Co-Generation (`gemini-4-argon`)**: Synthesizes **(a) system implementation**, **(b) immutable Z3 SMT safety invariants (`invariants_locked.py`)**, and **(c) 3D trajectory adapter** (`apps/api/agents/argon_synth.py`).
2. **Managed Agents Sandbox + Protected Hooks (`antigravity-preview-09-2026`)**: Runs Z3 inside an isolated sandbox (`apps/api/agents/managed_runner.py`). **Protected Hooks** (`apps/api/security/protected_hooks.py`) block invariant SHA-256 tampering, out-of-scope file writes, prompt-injection attacks, and secret leaks.
3. **3D Counterexample Replay & Surgical Self-Patch**: On `SAT_VIOLATION`, the Three.js Cockpit replays the exact violation millisecond (drone collision at `t=4.2s`, 3-DOF arm torque breach at `tick 28`, or `4×4×4` spatial deadlock at `tick 18`), then iteratively patches the controller until Z3 proves **`UNSAT_PROVEN`**.
4. **Credential Proxy & Signed Proof Certificates**: `apps/api/security/credential_proxy.py` issues a verifiable SHA-256 Proof Certificate (`GET /api/forge/certificate/{id}`) and proxies GitHub proof export with `credential_exposed: false` and `redacted: true`.

---

## 2. Quickstart (Single-Process Offline Demo & Verification)

```bash
# 1. Setup backend + frontend
python3 -m venv .venv
.venv/bin/pip install -e "./apps/api[dev]"
pnpm --dir apps/web install   # atau: npm --prefix apps/web install

# 2. Full verification gate (tsc + vite build + vitest + ruff + pytest)
bash scripts/verify.sh

# 3. Run single-process demo (serves built Three.js UI + FastAPI/SSE at http://127.0.0.1:8000)
bash scripts/demo-offline.sh

# 4. Run live TCP/HTTP/SSE E2E smoke test against running server
.venv/bin/python scripts/smoke_e2e.py --base-url http://127.0.0.1:8000 --require-ui
```

Untuk mengaktifkan mode live Gemini di Hari-H (`PROOFFORGE_MODE=live_gemini`):

```bash
cp .env.example .env
# Set GEMINI_API_KEY=... dan PROOFFORGE_MODE=live_gemini di .env (jangan commit .env)
.venv/bin/python scripts/preflight_gemini.py
```

---

## 3. Skenario Verifikasi 3D

| Skenario | Domain Z3 | Pelanggaran Awal (`SAT`) | Bukti Aman (`UNSAT`) |
| :--- | :--- | :--- | :--- |
| `drone_swarm` | Quadratic kinematics (tanpa `sqrt`) | Head-on gap `0.38m < 1.50m` @ `tick 42` (`4.2s`) | Dynamic stopping-envelope braking (`101 frames`) |
| `robot_arm` | Pure `QF_LIA` Taylor linearization | Elbow torque `|tau2| > 8.0 N·m` @ `tick 28` | Clamped reach & payload envelope (`41 frames`) |
| `spatial_tiling` | `Int` grid `4×4×4` mutual exclusion | Circular wait deadlock `W1↔W2` @ `tick 18` | Canonical lexicographic lock order (`21 frames`) |

---

## 4. Peta Dokumentasi

| Dokumen | Fungsi |
| :--- | :--- |
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Arsitektur 4-lapis, kontrak JSON/SSE, model keamanan Hooks & Proxy |
| [`docs/Z3-SCENARIO-MATH-SPECS.md`](./docs/Z3-SCENARIO-MATH-SPECS.md) | Spesifikasi matematika Z3 eksak untuk 3 skenario |
| [`docs/PREFLIGHT-CHECKLIST-NYC.md`](./docs/PREFLIGHT-CHECKLIST-NYC.md) | Runbook VPS staging (`--protocol http2`) & dry-run pitch 120 detik |
| [`docs/SUBMISSION-PORTAL-KIT.md`](./docs/SUBMISSION-PORTAL-KIT.md) | Isian portal Cerebral Valley & shotlist video cadangan |
| [`docs/HACKATHON-DAY-RUNBOOK.md`](./docs/HACKATHON-DAY-RUNBOOK.md) | Checklist pagi Hari-H & alur demo panggung |
| [`BACKLOG.md`](./BACKLOG.md) · [`HANDOFF.md`](./HANDOFF.md) | Tracking progres & state estafet antar agen |
