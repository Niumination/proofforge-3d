# Panduan Setup Repo GitHub & Sinkronisasi Awal

Ikuti langkah ini untuk menjadikan paket dokumentasi Phase 0 ini sebagai repositori GitHub resmi yang bisa dilacak dari laptop, **Hermes Agent (LightVela VPS)**, dan **OpenCode**.

---

## 1. Buat Repository Baru di GitHub

Buat repository baru di akun `Niumination`:
* **Nama repo:** `proofforge-3d`
* **Visibility:** `Public` (disarankan untuk submission hackathon & portofolio) atau `Private` sementara hingga hari-H, lalu dibuka `Public` saat submission.
* **Jangan** centang *Add a README / .gitignore* saat membuat di UI GitHub (karena sudah tersedia lengkap di folder ini).

---

## 2. Inisialisasi & Push dari Workspace Lokal

Jalankan perintah berikut di dalam folder `/home/user/proofforge-3d` (atau lokasi tempat kamu menyalin folder ini):

```bash
cd proofforge-3d
git init -b main
git add .
git status   # Pastikan TIDAK ada file .env atau kredensial
git commit -m "docs(pf-001): initialize ProofForge 3D architecture, scaffold blueprint, and multi-agent workflow"
git remote add origin https://github.com/Niumination/proofforge-3d.git
git push -u origin main
```

Atau jika menggunakan GitHub CLI (`gh`):

```bash
cd proofforge-3d
git init -b main
git add .
git commit -m "docs(pf-001): initialize ProofForge 3D architecture, scaffold blueprint, and multi-agent workflow"
gh repo create Niumination/proofforge-3d --public --source=. --remote=origin --push
```

---

## 3. Bootstrap di VPS LightVela (Untuk Hermes Agent)

Setelah repo berada di GitHub, jalankan (atau perintahkan Hermes Agent menggunakan prompt di `docs/MULTI-AGENT-WORKFLOW.md` §4.1):

```bash
mkdir -p ~/projects
cd ~/projects
git clone https://github.com/Niumination/proofforge-3d.git
cd proofforge-3d
```

Verifikasi bahwa seluruh dokumen utama ada dan terbaca:

```bash
ls -la
ls -la docs/
```

---

## 4. Checklist Sebelum Masuk Phase 1 (Membuka Kunci Coding)

Pastikan 4 hal berikut terpenuhi sebelum memberi sinyal ke OpenCode untuk menulis kode:
- [ ] Repo `Niumination/proofforge-3d` sudah ter-push ke GitHub.
- [ ] Hermes Agent di VPS LightVela sudah membaca `AGENTS.md`, `ARCHITECTURE.md`, dan `HANDOFF.md`.
- [ ] `BACKLOG.md` untuk `PF-003` dan `PF-004` sudah dicentang `[x]`.
- [ ] Kamu sudah meninjau 3 skenario di `docs/BRAINSTORMING-AND-DEMO-SCENARIOS.md` dan menyetujui struktur di `docs/SCAFFOLD-BLUEPRINT.md`.
