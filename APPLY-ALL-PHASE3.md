# Cara Menerapkan Seluruh Paket Phase 3 (`pkg1` → `pkg5`)

> **Penting:** Pastikan semua perubahan di-commit dan `git push origin main` agar GitHub & LightVela VPS sinkron!

```bash
cd ~/projects/proofforge-3d
git checkout main && git pull --ff-only origin main

unzip -o /path/to/proofforge-phase3-pkg1-argon-cogenerator.zip -d .
unzip -o /path/to/proofforge-phase3-pkg2-managed-agents-hooks-proxy.zip -d .
unzip -o /path/to/proofforge-phase3-pkg3-closed-loop-redteam-voice.zip -d .
unzip -o /path/to/proofforge-phase3-pkg4-cockpit-pro-ui-and-judgekit.zip -d .
unzip -o /path/to/proofforge-phase3-pkg5-polish-and-submission.zip -d .

.venv/bin/pip install -e "./apps/api[dev]"
bash scripts/verify.sh
bash scripts/vps-stage.sh
```

Commit & push ke GitHub setelah lulus:

```bash
git add -A
git commit -m "feat(phase3): apply pkg1..pkg5 (Argon, Managed Agents, Hooks/Proxy, Cockpit Pro, Submission Kit)"
git push origin main
```
