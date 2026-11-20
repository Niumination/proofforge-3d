# ProofForge 3D — Phase 1 Tested Overlay Package (`PF-005`..`PF-014`, `PF-017`)

Overlay ini berisi implementasi lengkap Phase 1 (Non-AI Core + Real Z3 Scenarios + Three.js 3D Cockpit UI) yang telah lolos seluruh gate di `scripts/verify.sh`.

## Cara Menerapkan di Branch `feat/pf-005-phase1` (OpenCode / Lokal / VPS)

```bash
cd ~/projects/proofforge-3d   # atau folder repo lokal Anda
git fetch origin
git checkout feat/pf-005-phase1

# 1. Ekstrak overlay menimpa file scaffold yang rusak/stub
unzip -o /path/to/proofforge-phase1-complete-overlay.zip -d .

# 2. Setup Python venv & Node dependencies
python3 -m venv .venv
.venv/bin/pip install -e "./apps/api[dev]"
pnpm --dir apps/web install   # atau: npm --prefix apps/web install

# 3. Jalankan full verification gate
bash scripts/verify.sh
```

## Catatan Penting Push GitHub (`.github/workflows/ci.yml`)

Pada commit sebelumnya (`09442e4`), `.github/workflows/ci.yml` di-drop karena token OAuth tidak memiliki scope `workflow`.
Jika `git push` ditolak GitHub dengan pesan `refusing to allow an OAuth App to create or update workflow .github/workflows/ci.yml`, Anda bisa:
- Push menggunakan SSH key atau PAT dengan scope `workflow`, **ATAU**
- Hapus sementara `.github/workflows/ci.yml` dari commit (`git rm --cached .github/workflows/ci.yml`) lalu tambahkan langsung via GitHub Web UI.

## Hasil Uji Terverifikasi Sebelum Packaging

- `tsc -b --noEmit` → 0 errors
- `vite build` → built cleanly (`dist/`)
- `vitest run` → 2 passed (`src/App.test.tsx`)
- `ruff check apps/api scenarios sandbox-agent` → All checks passed
- `pytest apps/api -v` → 5 passed (`drone_swarm`, `robot_arm`, `spatial_tiling`, `invariant_guard`, FastAPI SSE + export)
