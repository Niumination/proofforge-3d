# Cara Menerapkan Paket Terakhir (`pkg7`) di Atas `main` (`a364cb3`)

```bash
cd ~/projects/proofforge-3d
git checkout main && git pull --ff-only origin main

unzip -o /path/to/proofforge-phase3-pkg7-final-polish-and-ui-render-tests.zip -d .

bash scripts/vps-stage.sh
git add -A
git commit -m "feat(phase3): pkg7 — final UI polish, React UI render test, pitch quick-card, backlog sync"
git push origin main
```

Lalu jalankan demo offline/lokal untuk rekam video (`PF-028`) & panggung (`PF-029`):

```bash
bash scripts/demo-offline.sh
# Buka http://127.0.0.1:8000
```
