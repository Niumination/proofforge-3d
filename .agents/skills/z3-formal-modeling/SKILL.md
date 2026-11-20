# Z3 Formal Modeling — ProofForge 3D

Aturan pemodelan Z3 untuk skenario ProofForge 3D. Wajib dibaca sebelum menulis `invariants_locked.py`, `buggy_impl.py`, `fixed_impl.py`, atau `scene_adapter.py`.

- Domain variabel: semua `Real`, ranges terkunci (drone: `v in [10,15] m/s`, latency `[0.05,0.30] s`; arm: torsi linier; tiling: spawn).
- Kontrak invarian: ditulis sebagai assertion pasti, hash SHA-256 di-lock di `invariants_locked.py`.
- Counterexample (SAT) & fix proof (UNSAT): memakai rumus linier & linearisasi `y_eff` (anti Z3 timeout).
- JANGAN tambah sqrt di model drone_swarm (head-on kuadratik) — gunakan linearisasi numerik yang sudah terkalibrasi.
- Timeout solver: 8000 ms per run; timeout tercapai → status `ERROR`.
