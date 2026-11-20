---
name: z3-counterexample-patcher
description: Run Z3 verification in sandbox and patch implementation from counterexample traces.
---
# Z3 Counterexample Patcher
1. Compute SHA-256 of `invariants_locked.py` before & after every run.
2. Run `z3_harness.py` with 8000ms timeout.
3. On SAT: extract counterexample variables and patch `system_impl.py`.
4. On UNSAT: emit Proof Certificate via Credential Proxy.
