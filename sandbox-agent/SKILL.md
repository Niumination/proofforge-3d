# Skill: Z3 & Surgical Patch di Sandbox
- Runner: `python3 z3_runner.py` dengan timeout maksimal 8000 ms.
- Sebelum solver: jalankan `pre_verify_guard.py` (SHA-256 check).
- Setelah SAT: scene_adapter membentuk counterexample frame; patcher menjalankan surgical patch.
- Setelah UNSAT: agent status `PROVEN_SAFE`.
