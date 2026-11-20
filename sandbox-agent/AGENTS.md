# Antigravity Managed Agent Instructions (ProofForge 3D)

You are running inside an isolated Google Managed Agents Linux sandbox (`antigravity-preview-09-2026`).
1. Never modify `invariants_locked.py` — Protected Hooks enforce SHA-256 immutability.
2. Execute Z3 verification via `python3 z3_harness.py` and parse SAT counterexamples.
3. Apply surgical patches ONLY inside `workspace/impl/` until Z3 returns `UNSAT`.
