# Three.js Counterexample UI — ProofForge 3D

Kebijakan visualisasi frame merah & time scrubber untuk ProofForge 3D.

- Frame dirinya: `SceneTimelineFrame[]` (tick, time_sec, is_violation, entities, constraints_overlay).
- Safety sphere: wireframe, hijau (`R_safe`) → merah (`breached: true`) saat `is_violation`.
- TimeScrubber: play/pause, speed, lompat ke `violated_tick`, Before (SAT) / After (UNSAT).
- Viewport harus browser-safe: hanya relative `/api/...`, tanpa hardcode localhost.
- Latensi demo: deterministic < 1.5 detik dari Run ke frame 3D.
