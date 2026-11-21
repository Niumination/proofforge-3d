# ProofForge 3D — Pre-Flight Staging & 2-Minute NYC Pitch Dry-Run (`PF-015`..`PF-018`)

## 1. Perintah Hermes Agent @ LightVela VPS (`PF-015` & `PF-016`)

Jalankan di `~/projects/proofforge-3d` (terisolasi dari OMB/9Router):

```bash
cd ~/projects/proofforge-3d
git fetch origin
git checkout main
git pull --ff-only origin main

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
| **0:00 – 0:25** | Pilih **Drone Swarm Collision**, klik **1-Click Stage Auto-Demo**. | *"AI coding agents generate code that looks fine until an edge case hits. Watch Z3 catch a head-on collision at 4.2s with 3D velocity vectors and shockwaves, then auto-patch to `UNSAT`."* |
| **0:25 – 0:50** | Tekan `[B]` untuk kembali ke **BEFORE**, tekan `[F]` (**Focus Violation**), lalu buka **Inspect Surgical Patch Diff** (`Copy Diff`). | *"First, our Protected Hook blocks reward-hacking attempts to weaken `R_safe`. Then Z3 pinpoints the exact SAT frame at 0.38m separation and patches only the controller—never the locked invariant."* |
| **0:50 – 1:15** | Klik **Simulate Prompt Injection Attack**, lalu klik **Download Audit Report (.md)** & **Inspect Signed Proof Certificate**. | *"Every run is guarded by Managed Agents Protected Hooks and a Credential Proxy that issues a SHA-256 Proof Certificate and Markdown Audit Report with zero token exposure."* |
| **1:15 – 1:45** | Klik preset **"Limit robot arm payload to 3.0 kg"** → **Run ProofForge Pipeline** (3D articulated robot arm + torque overload halo). | *"Voice constraints dynamically re-parameterize both the Z3 solver and the 3D safety envelope across drones, robot arms, and 4×4×4 spatial grids."* |
| **1:45 – 2:00** | Tunjukkan `PROXY_AUDIT` (`credential_exposed: false`) & closing statement. | *"Code isn't done when it compiles—it's done when Z3 proves `UNSAT`."* |
