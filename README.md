# ProofForge 3D

> **Self-Verifying Systems Compiler & 3D Visual Counterexample Engine**  
> Built for **Gemini 4 NYC Hackathon** (Cerebral Valley × Google DeepMind — Nov 21, 2026)

[![Target Event](https://img.shields.io/badge/Event-Gemini%204%20NYC%20Hackathon-4285F4)](#)
[![Track](https://img.shields.io/badge/Tracks-Advanced%20Reasoning%20%7C%20Visual%20Coding%20%7C%20Managed%20Agents-34A853)](#)
[![Status](https://img.shields.io/badge/Build-Phase%201--5%20Verified%20(24%20Pytest%20%2B%20Vitest)-00C853)](#)

---

## 1. Visi & Arsitektur Closed-Loop

AI coding agents write code that compiles and looks right—until edge-case physics, actuator torque limits, or concurrency deadlocks fail catastrophically. **ProofForge 3D** closes that gap:

1. **Co-Generation (`gemini-4-argon`)**: Synthesizes **(a) system implementation**, **(b) immutable Z3 SMT safety invariants (`invariants_locked.py`)**, and **(c) 3D trajectory adapter** (`apps/api/agents/argon_synth.py`).
2. **Managed Agents Sandbox + Protected Hooks (`antigravity-preview-09-2026`)**: Runs Z3 inside an isolated sandbox (`apps/api/agents/managed_runner.py`). **Protected Hooks** (`apps/api/security/protected_hooks.py`) block invariant SHA-256 tampering, out-of-scope file writes, prompt-injection attacks, and secret leaks.
3. **3D Counterexample Replay & Surgical Self-Patch**: On `SAT_VIOLATION`, the Three.js Cockpit replays the exact violation millisecond—complete with **velocity vectors, collision shockwave rings, 3D articulated cylinder arm links + torque overload halo, and deadlock dependency arrows**—then iteratively patches the controller until Z3 proves **`UNSAT_PROVEN`**.
4. **Dynamic Parametric Z3 Constraints**: Voice or spec overrides (`r_safe_m=2.2m`, `payload_kg=3.0kg`, `max_wait_ticks=2`) dynamically re-parameterize both Z3 solving and 3D safety envelopes in real time.
5. **Credential Proxy, Proof Certificates & Formal Audit Reports**: `apps/api/security/credential_proxy.py` issues a verifiable SHA-256 Proof Certificate (`GET /api/forge/certificate/{id}`), serves a downloadable Markdown audit report (`GET /api/forge/report/{id}`), and proxies GitHub export with `credential_exposed: false` and `redacted: true`.

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

### Stage Hotkeys & Auto-Demo
* **1-Click Stage Auto-Demo**: Runs the full closed loop, auto-plays the red `SAT_VIOLATION` crash, transitions to `AFTER · PATCHED (UNSAT)`, and exports the signed proof certificate.
* **Keyboard Shortcuts**: `[Space]` Play/Pause · `[F]` Focus Violation · `[B]` Toggle Before/After · `[Esc]` Close Modals.

---

## 3. Skenario Verifikasi 3D

| Skenario | Domain Z3 | Pelanggaran Awal (`SAT`) | Bukti Aman (`UNSAT`) |
| :--- | :--- | :--- | :--- |
| `drone_swarm` | Quadratic kinematics (tanpa `sqrt`) | Head-on gap `0.38m < r_safe_m` @ `tick 42` (`4.2s`) | Dynamic stopping-envelope braking (`101 frames`) |
| `robot_arm` | Pure `QF_LIA` Taylor linearization | Elbow torque `|tau2| > 8.0 N·m` @ `tick 28` | Clamped reach & payload envelope (`41 frames`) |
| `spatial_tiling` | `Int` grid `4×4×4` mutual exclusion | Circular wait deadlock `W1↔W2` @ `tick 18` | Canonical lexicographic lock order (`21 frames`) |
