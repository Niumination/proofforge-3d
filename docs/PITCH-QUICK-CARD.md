# ProofForge 3D — 1-Page Judge & Pitch Quick-Card (`PF-029`)

## 30-Second Core Hook
> *"AI coding agents write code that compiles and looks right—until an edge case hits. **ProofForge 3D** co-generates code, an immutable Z3 SMT invariant, and a 3D failure replay. When Z3 finds a SAT counterexample—like two drones colliding at 4.2 seconds—we replay that exact frame in Three.js, surgically patch the controller inside a Managed Agents sandbox guarded by Protected Hooks, and prove `UNSAT` across the entire domain."*

## Top 4 Judge Q&A Answers
1. **Why Z3 instead of unit tests or an LLM judge?**
   Unit tests only sample inputs you thought of; Z3 searches the **entire mathematical domain** (`∀ v_A, v_B, latency`) and either produces a concrete `SAT` counterexample or an exhaustive `UNSAT` proof.
2. **How do you stop the AI from cheating by weakening the safety threshold?**
   **Protected Hooks** (`apps/api/security/protected_hooks.py`) lock `invariants_locked.py` with SHA-256 + enforce `write_scope_guard` + block prompt-injection attempts (`HOOK_AUDIT: BLOCKED`). Click **"Simulate Prompt Injection Attack"** to watch 5 blocks fire live!
3. **Why does this fit Best Use of Managed Agents ($5,000)?**
   We implement the full Managed Agents architecture (`antigravity-preview-09-2026`): `AGENTS.md`/`SKILL.md` sandbox execution, **Protected Hooks** for invariant immutability, and a **Credential Proxy** (`credential_proxy.py`) that signs `UNSAT` Proof Certificates and exports to GitHub with `credential_exposed: false` & `redacted: true`.
4. **What happens if venue Wi-Fi or external LLM latency spikes?**
   `ClosedLoopOrchestrator` runs both `live_gemini` (`gemini-4-argon` + `gemini-3.8-flash`) AND an instant local Z3 deterministic engine served from a single offline process (`bash scripts/demo-offline.sh` @ `http://127.0.0.1:8000`).
