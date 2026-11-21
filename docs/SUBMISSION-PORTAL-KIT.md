# ProofForge 3D — Cerebral Valley Submission & Judging Kit (`PF-028`, `PF-029`)

## 1. Ready-to-Paste Submission Fields

* **Project Name:** `ProofForge 3D`
* **One-Line Tagline:** `Self-verifying systems compiler that turns Z3 formal counterexamples into 3D failure replays and self-patches code until proven UNSAT.`
* **Tracks Targeted:**
  1. **Main Track** (Advanced Reasoning + Visual Coding + Robotics + World Models)
  2. **Best Use of Managed Agents ($5,000)** (`antigravity-preview-09-2026` + Protected Hooks + Credential Proxy)

### Short Description (Portal Box)
> AI coding agents write code that compiles and looks plausible—until physics, torque limits, or concurrency deadlocks break in production. **ProofForge 3D** co-generates system code, an immutable Z3 SMT safety invariant (`invariants_locked.py`), and a 3D trajectory adapter using **Gemini 4 Argon**. Inside an isolated **Managed Agents** sandbox guarded by **Protected Hooks**, Z3 searches the entire state space for an exact `SAT` counterexample, replays the exact millisecond of collision/overload/deadlock in an interactive **Three.js 3D Cockpit**, and applies surgical patches until Z3 proves `UNSAT` across all inputs—then exports a SHA-256 **Proof Certificate** via a **Credential Proxy** with zero secret exposure.

### Best Use of Managed Agents Justification
* **Protected Hooks (`apps/api/security/protected_hooks.py`):** Blocks reward-hacking (modifying `invariants_locked.py` SHA-256), out-of-scope file writes, and prompt-injection exfiltration attempts in real time (`HOOK_AUDIT: BLOCKED`).
* **Credential Proxy (`apps/api/security/credential_proxy.py`):** Holds GitHub export credentials strictly outside the LLM/agent context (`credential_exposed: false`, `redacted: true`) and signs verifiable `UNSAT_PROVEN` Proof Certificates.
* **Isolated Sandbox Execution (`apps/api/agents/managed_runner.py`):** Parity between `antigravity-preview-09-2026` Interactions API and isolated local subprocess execution.

---

## 2. 120-Second Backup Video Shotlist (`PF-028`)

1. **0:00–0:15:** Show 3-pane Cockpit (`http://127.0.0.1:8000`) + click **Run ProofForge Pipeline** on `Drone Swarm Collision`.
2. **0:15–0:40:** Red vignette flash at `tick 42 (t = 4.2s)` with `0.38m` separation laser line → click **Focus Violation**.
3. **0:40–1:05:** Click **Simulate Prompt Injection Attack** → show 5 `HOOK_AUDIT: BLOCKED` cards (`pre_verify_invariant_guard`, `write_scope_guard`, `red_team_prompt_guard`).
4. **1:05–1:35:** Toggle **AFTER · PATCHED (UNSAT)**, open **Inspect Surgical Patch Diff**, and inspect **Signed Proof Certificate**.
5. **1:35–2:00:** Use **Voice / Natural Constraint** (`"Limit robot arm payload to 3.0 kg"`), run **Export Proof via Credential Proxy**, show `redacted: true`.
