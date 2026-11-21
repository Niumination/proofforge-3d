# ProofForge 3D — Cerebral Valley Submission & Judging Kit (`PF-028`, `PF-029`)

## 1. Ready-to-Paste Submission Fields

* **Project Name:** `ProofForge 3D`
* **One-Line Tagline:** `Self-verifying systems compiler that turns Z3 formal counterexamples into 3D failure replays and self-patches code until proven UNSAT.`
* **Tracks Targeted:**
  1. **Main Track** (Advanced Reasoning + Visual Coding + Robotics + World Models)
  2. **Best Use of Managed Agents ($5,000)** (`antigravity-preview-09-2026` + Protected Hooks + Credential Proxy)

### Short Description (Portal Box)
> AI coding agents write code that compiles and looks plausible—until physics, torque limits, or concurrency deadlocks break in production. **ProofForge 3D** co-generates system code, an immutable Z3 SMT safety invariant (`invariants_locked.py`), and a 3D trajectory adapter using **Gemini 4 Argon**. Inside an isolated **Managed Agents** sandbox guarded by **Protected Hooks**, Z3 searches the entire state space for an exact `SAT` counterexample, replays the exact millisecond of collision/overload/deadlock in an interactive **Three.js 3D Cockpit** (with velocity vectors, shockwave rings, 3D articulated robot links, and deadlock arrows), and applies surgical patches until Z3 proves `UNSAT` across all inputs—then exports a SHA-256 **Proof Certificate** and downloadable **Formal Audit Report** via a **Credential Proxy** with zero secret exposure.

### Best Use of Managed Agents Justification
* **Protected Hooks (`apps/api/security/protected_hooks.py`):** Blocks reward-hacking (modifying `invariants_locked.py` SHA-256), out-of-scope file writes, and prompt-injection exfiltration attempts in real time (`HOOK_AUDIT: BLOCKED`).
* **Credential Proxy (`apps/api/security/credential_proxy.py`):** Holds GitHub export credentials strictly outside the LLM/agent context (`credential_exposed: false`, `redacted: true`) and signs verifiable `UNSAT_PROVEN` Proof Certificates + `.md` Audit Reports.
* **Isolated Sandbox Execution (`apps/api/agents/managed_runner.py`):** Parity between `antigravity-preview-09-2026` Interactions API and isolated local subprocess execution.

---

## 2. 120-Second Backup Video Shotlist (`PF-028`)

1. **0:00–0:20:** Show 3-pane Cockpit (`http://127.0.0.1:8000`) + click **1-Click Stage Auto-Demo** on `Drone Swarm Collision` (shows velocity vectors + red shockwave ring at `tick 42`, then auto-switches to green `UNSAT_PROVEN`).
2. **0:20–0:45:** Click **Focus Violation** (`F`) and **Toggle Before/After** (`B`), open **Inspect Surgical Patch Diff** (`Copy Diff`).
3. **0:45–1:10:** Click **Simulate Prompt Injection Attack** → show 5 `HOOK_AUDIT: BLOCKED` cards (`pre_verify_invariant_guard`, `write_scope_guard`, `red_team_prompt_guard`).
4. **1:10–1:35:** Click **Signed Proof Certificate** → **Download Audit Report (.md)** & show `Convergence Summary (SAT @ tick 42 → UNSAT)`.
5. **1:35–2:00:** Click voice preset **"Limit robot arm payload to 3.0 kg"** → **Run ProofForge Pipeline** (3D articulated robot arm + torque overload halo) → **Export Proof via Credential Proxy** (`redacted: true`).
