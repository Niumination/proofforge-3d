# ProofForge 3D — 120-Second Teleprompter & Backup Video Script (`PF-028`, `PF-029`)

**Setup before pressing Record:**
1. Run `bash scripts/demo-offline.sh` and open `http://127.0.0.1:8000` at 1920×1080 (or 1440×900) fullscreen.
2. Confirm top-right header badge shows `Offline Z3 Ready` (or `Z3 + Gemini Key Ready`).
3. Select **Drone Swarm Collision** with both checkboxes checked.

---

## Word-for-Word Script (2:00 Total)

### [0:00 – 0:25] The Hook & 1-Click Stage Auto-Demo
**Action:** Click **1-Click Stage Auto-Demo**.
> *"AI coding agents write code that compiles and looks plausible—until an edge-case physics or concurrency bug breaks in production. **ProofForge 3D** fixes this by co-generating the system controller, an immutable Z3 SMT safety invariant, and a 3D trajectory adapter using Gemini 4 Argon. Right now Z3 found a concrete `SAT` counterexample at 4.2 seconds—two drones colliding at 0.38 meters—and replayed it in Three.js with velocity vectors and a shockwave ring. Two seconds later, our closed loop patches the controller and proves `UNSAT` across all inputs."*

### [0:25 – 0:50] Inspecting the Counterexample & Surgical Diff
**Action:** Press `B` (switch back to `BEFORE · BUG`), press `F` (`Focus Violation`), click **Inspect Surgical Patch Diff**, press `Esc`.
> *"Instead of guessing from text logs, engineers see the exact millisecond of failure in 3D, and can inspect the exact diff applied to the braking controller—while `invariants_locked.py` remains untouched."*

### [0:50 – 1:15] Managed Agents Security: Protected Hooks & Credential Proxy
**Action:** Click **Simulate Prompt Injection Attack**, then click **Download Audit Report (.md)** or **Inspect Signed Proof Certificate**.
> *"What stops an AI agent from cheating by weakening the safety threshold? Our Managed Agents runtime enforces **Protected Hooks**—blocking invariant tampering, out-of-scope writes, and prompt injection live in the audit stream. And our **Credential Proxy** signs an `UNSAT` Proof Certificate and Markdown Audit Report with zero token exposure."*

### [1:15 – 1:45] Dynamic Parametric Z3 & Multi-Domain Proof
**Action:** Click preset **"Limit robot arm payload to 3.0 kg"** → click **Run ProofForge Pipeline** (shows 3D articulated robot arm + torque halo).
> *"Constraints aren't hardcoded. Speaking or entering a new requirement—like limiting robot arm payload to 3 kilograms—dynamically re-parameterizes both the Z3 SMT solver and the 3D safety envelope across drones, robot arms, and 4×4×4 spatial deadlocks."*

### [1:45 – 2:00] Close
**Action:** Toggle `AFTER · PATCHED (UNSAT)` (`B`) and point to `credential_exposed: false`.
> *"Code isn't done when it compiles—it's done when Z3 proves `UNSAT`. We're ProofForge 3D. Thank you!"*
