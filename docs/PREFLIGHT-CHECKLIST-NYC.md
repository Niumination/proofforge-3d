# ProofForge 3D — Pre-Flight Staging & 2-Minute NYC Pitch Dry-Run (`PF-015`..`PF-018`)

## 1. Perintah Hermes Agent @ LightVela VPS (`PF-015` & `PF-016`)

Jalankan di `~/projects/proofforge-3d` (terisolasi dari OMB/9Router):

```bash
cd ~/projects/proofforge-3d
git fetch origin
git checkout feat/pf-005-phase1
git pull --ff-only origin feat/pf-005-phase1

bash scripts/vps-stage.sh
```

Jika ingin staging publik sementara via Cloudflare Quick Tunnel (wajib `--protocol http2` sesuai `AGENTS.md`):

```bash
bash scripts/demo-offline.sh &
bash scripts/vps-tunnel.sh
```

---

## 2. Mode Offline Single-Process di Laptop Demo (Fallback Anti-Wi-Fi Venue)

FastAPI otomatis menyajikan bundle produksi `apps/web/dist` pada `http://127.0.0.1:8000`:

```bash
bash scripts/demo-offline.sh
# Buka browser: http://127.0.0.1:8000
```

* **Zero CORS / Zero Vite Dev Server** di panggung.
* **100% Deterministik Z3** (`z3-solver` lokal) jika koneksi ke `gemini-4-argon` atau `antigravity-preview-09-2026` terganggu.

---

## 3. Naskah Dry-Run 120 Detik (`PF-018`)

| Waktu | Aksi di Layar Cockpit | Poin Narasi Juri |
| :--- | :--- | :--- |
| **0:00 – 0:20** | Pilih **Drone Swarm Collision**, pastikan kedua checkbox ON, klik **Run ProofForge Pipeline**. | *"AI coding agents generate code that looks fine until an edge case hits. Watch Z3 catch a head-on collision before runtime."* |
| **0:20 – 0:45** | Sorot panel kanan (`HOOK_AUDIT: BLOCKED`) lalu viewport flash merah pada **tick 42 (t = 4.2s)**. Klik **Focus Violation**. | *"First, our Protected Hook blocks a simulated reward-hacking attempt to weaken `R_safe`. Then Z3 finds an exact SAT counterexample at 4.2 seconds—0.38m separation."* |
| **0:45 – 1:15** | Klik **Inspect Surgical Patch Diff**, lalu klik toggle **AFTER · PATCHED (UNSAT)** dan tekan **Play**. | *"ProofForge patches only the stopping-envelope controller—never the locked invariant—and Z3 proves `UNSAT` across all speeds and latencies."* |
| **1:15 – 1:40** | Pindah cepat ke **3-DOF Robot Arm** (atau **4×4×4 Spatial Deadlock**), lalu klik **Export Proof via Credential Proxy**. | *"The exact same formal-to-3D loop works for 3-DOF torque limits and 3D spatial deadlocks, exporting a signed proof with zero token exposure."* |
| **1:40 – 2:00** | Tunjukkan `PROXY_AUDIT` (`credential_exposed: false`) & closing statement. | *"Code isn't done when it compiles—it's done when Z3 proves `UNSAT`."* |

---

## 4. Checklist Transisi ke Phase 3 (Hackathon Day · Sabtu 21 Nov 2026 · 09:00 EST)

- [ ] Klaim API key Google DeepMind di venue, isi `.env` lokal (`GEMINI_API_KEY`, `PROOFFORGE_MODE=live_gemini`).
- [ ] Pastikan `.env` tidak pernah masuk `git status` (`.gitignore` sudah memblokir).
- [ ] Mulai `PF-020` (`argon_synth.py`) dan `PF-021` (`managed_runner.py` untuk `antigravity-preview-09-2026`).
