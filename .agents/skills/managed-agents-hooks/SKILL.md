# Managed Agents Hooks — ProofForge 3D

Konvensi Protected Hooks & Credential Proxy untuk Phase 3 (Google Managed Agents).

- `pre_verify_guard.py`: cek SHA-256 hash `invariants_locked.py` sebelum solver jalan; BLOCKED jika tamper.
- `write_scope_guard.py`: tolak penulisan di luar `workspace/impl/` dan `workspace/skills/`.
- Credential Proxy: secret lewat proxy (dummy token di sandbox, token asli hanya ke domain allowlist, e.g. api.github.com).
- Iteration budget: max 5, Z3 timeout 8000 ms per pass.
