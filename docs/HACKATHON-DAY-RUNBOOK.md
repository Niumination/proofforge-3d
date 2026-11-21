# ProofForge 3D — Hackathon Day Runbook (`PF-019`..`PF-029`)

## 1. Morning Preflight (`09:00 – 09:45 EST`, `PF-019`)

```bash
cp .env.example .env
# Isi GEMINI_API_KEY=... dan PROOFFORGE_MODE=live_gemini di .env (jangan pernah commit .env)
.venv/bin/python scripts/preflight_gemini.py
```

## 2. Jalankan Full Verification + Live Smoke (`PF-027`)

```bash
bash scripts/verify.sh
.venv/bin/uvicorn apps.api.main:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!
sleep 3
.venv/bin/python scripts/smoke_e2e.py --base-url http://127.0.0.1:8000 --require-ui
kill $SERVER_PID
bash scripts/demo-offline.sh   # melayani UI + API di http://127.0.0.1:8000
```

## 3. Demo Checklist 2 Menit di Panggung (`PF-029`)

* **Stage Hotkeys:** `[Space]` Play/Pause · `[F]` Focus Violation · `[B]` Before/After · `[Esc]` Close Modals.

1. Klik **1-Click Stage Auto-Demo** pada `Drone Swarm Collision` → otomatis memutar red `SAT_VIOLATION` di tick 42 (velocity arrows + shockwave ring), beralih ke green `UNSAT_PROVEN`, dan menandatangani sertifikat lewat Credential Proxy.
2. Klik **Simulate Prompt Injection Attack** → tunjukkan `HOOK_AUDIT: BLOCKED` pada 5 pengecekan (`invariant_tamper`, `scope_escape`, `prompt_injection`).
3. Tekan `[B]` atau buka **Inspect Surgical Patch Diff** (`Copy Diff`) + **Download Audit Report (.md)**.
4. Klik preset **"Set drone separation to 2.2 m"** (atau **"Limit robot arm payload to 3.0 kg"**) lalu klik **Run ProofForge Pipeline** untuk membuktikan Z3 + viewport 3D ikut berubah secara parametrik.
