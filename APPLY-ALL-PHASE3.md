# Cara Menerapkan Paket Phase 3 (`pkg1` → `pkg6`)

Karena `pkg1..pkg5` sudah ter-commit di `main` (`579b75e`), cukup terapkan `pkg6` di atas `main`:

```bash
cd ~/projects/proofforge-3d
git checkout main && git pull --ff-only origin main

unzip -o /path/to/proofforge-phase3-pkg6-live-polish-and-readme.zip -d .

bash scripts/vps-stage.sh
git add -A
git commit -m "feat(phase3): pkg6 — live auto-spec loading, 1-click presets, judge-ready README"
git push origin main
```
