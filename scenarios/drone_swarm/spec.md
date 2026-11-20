# Skenario A — drone_swarm (HERO DEMO)

- Deskripsi: koordinasi swarm quadrotor, invarian `min pairwise distance >= R_safe`.
- Buggy impl: naive latency compensation → tidak pernah mendeteksi (SAT counterexample).
- Fixed impl: dynamic stopping-envelope braking → UNSAT.
- Scene adapter: quadrotor 3D + safety sphere wireframe + red frame.
