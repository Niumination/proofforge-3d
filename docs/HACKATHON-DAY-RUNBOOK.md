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
bash scripts/demo-offline.sh   # melayani UI + API di http://127.0.0.1:8000
```

## 3. Demo Checklist 2 Menit di Panggung (`PF-029`)

1. Klik **Run ProofForge Pipeline** pada `Drone Swarm Collision` → tunjukkan `SAT_VIOLATION` di tick 42 + laser merah antar drone.
2. Klik **Simulate Prompt Injection Attack** → tunjukkan `HOOK_AUDIT: BLOCKED` pada 3 vektor serangan (`invariant_tamper`, `scope_escape`, `prompt_injection`).
3. Toggle **AFTER · PATCHED (UNSAT)** + klik **Inspect Surgical Patch Diff** + **Inspect Signed Proof Certificate**.
4. Ketik atau ucapkan constraint di **Voice / Natural Constraint** (`"Limit robot arm payload to 3.0 kg"`) lalu klik **Export Proof via Credential Proxy**.
