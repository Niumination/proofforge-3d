# Multi-Agent Workflow Playbook — Ekosistem LightVela, OpenCode, Arena.ai & Cerebral Valley

Dokumen ini menyusun **alur kerja tanpa bentrok (*conflict-free*)** antara keempat sistem AI yang kamu gunakan sebelum dan selama hackathon.

---

## 1. Peta Ekosistem & Peran Masing-Masing Platform

```
                       ┌──────────────────────────────────────┐
                       │   GITHUB (Single Source of Truth)    │
                       │    Niumination/proofforge-3d         │
                       └──┬──────────▲───────────▲─────────┬──┘
                          │          │           │         │
         ┌────────────────┘          │           │         └────────────────┐
         ▼                           │           │                          ▼
┌─────────────────┐        ┌─────────┴──┐   ┌────┴───────────┐     ┌─────────────────────┐
│   ARENA.AI      │        │  OPENCODE  │   │  HERMES AGENT  │     │ CEREBRAL VALLEY /   │
│                 │        │  (Lokal /  │   │  (LightVela    │     │ GOOGLE DEEPMIND     │
│ • Arsitektur    │        │   IDE)     │   │   VPS 24/7)    │     │                     │
│ • Spec & Z3     │        │            │   │                │     │ • Kredit API Venue  │
│   Math Design   │        │ • Coding   │   │ • Sync & Pull  │     │ • Gemini 4 Argon    │
│ • Audit Diff &  │        │   per task │   │ • Verify Gate  │     │ • Managed Agents    │
│   Keamanan      │        │ • Typecheck│   │ • Staging/HTTP2│     │   (Antigravity)     │
│ • Pitch & Demo  │        │ • Unit Test│   │ • Update State │     │ • Gallery Submit    │
└─────────────────┘        └────────────┘   └────────────────┘     └─────────────────────┘
```

### Mengapa Pembagian Ini Optimal?
1. **Arena.ai** unggul untuk *deep reasoning*, perancangan arsitektur, penyusunan logika Z3 yang bebas *false positive*, audit lintas file, dan penulisan materi pitch.
2. **OpenCode** (di mesin lokal / terminal IDE kamu, selaras dengan workflow `Flame-ADE`) paling cepat untuk mengeksekusi tugas coding interaktif per *task ID* (`PF-005` s.d. `PF-014`).
3. **Hermes Agent di VPS LightVela** selalu aktif 24/7 — sangat ideal sebagai **CI/Verification Runner, GitHub Tracker, dan Staging Host** di VPS milikmu (terpisah rapi dari runtime `openmausbot` / `9router` di `zbmaus-vela`), sekaligus bisa diakses dari mana saja lewat GitHub/Telegram saat kamu dalam perjalanan ke NYC.
4. **Platform Cerebral Valley / Google DeepMind** menjadi **target eksekusi live pada 21 November 2026** (klaim kredit, endpoint `gemini-4-argon` & `antigravity-preview-09-2026`, serta pengumpulan final).

---

## 2. Protokol Anti-Bentrok (Wajib Dipatuhi Semua Agen)

Karena ada lebih dari satu agen yang dapat menyentuh GitHub:
1. **Aturan Kunci Kepemilikan (*Write Lock*):**
   * Hanya **satu agen** yang menulis ke branch `feat/pf-XXX` pada satu waktu.
   * Sebelum bekerja, agen wajib melakukan `git pull --rebase` dan membaca **`HANDOFF.md`** serta **`BACKLOG.md`**.
   * **OpenCode** bertugas di branch fitur (`feat/pf-XXX`), sedangkan **Hermes Agent (LightVela VPS)** bertugas melakukan `git fetch`, menjalankan `scripts/verify.sh`, dan memperbarui status `[x]` serta `HANDOFF.md` (atau menggarap task infrastruktur VPS khusus seperti `PF-004`, `PF-015`, `PF-016`).
2. **Aturan Isolasi LightVela VPS:**
   * Clone repo di direktori kerja khusus proyek, misalnya `~/projects/proofforge-3d` (jangan di dalam direktori runtime OMB/9Router).
   * Jika ingin mem-publish staging preview lewat Cloudflare Tunnel di VPS LightVela, wajib gunakan `--protocol http2` (mencegah putusnya koneksi SSE stream dan payload JSON besar).
   * Jangan pernah mem-commit file `.env`, key 9Router, atau token OMB ke GitHub.

---

## 3. Alur Eksekusi End-to-End (Phase 0 → Phase 3)

### Tahap A — Bootstrap GitHub & LightVela VPS (Hari Ini: 17 Nov)
1. Kamu membuat repo GitHub `Niumination/proofforge-3d` dan mengunggah folder dokumentasi Phase 0 ini.
2. Kamu mengirim **Prompt Handoff ke Hermes Agent (LightVela VPS)** untuk meng-clone repo, menyiapkan `.venv` Python + `z3-solver` + Node di VPS, lalu mencatat kesiapan di `HANDOFF.md`.

### Tahap B — Pembangunan Pondasi Non-AI (18–19 Nov)
1. Kamu mengarahkan **OpenCode** mengerjakan task `PF-005` s.d. `PF-014` (satu task atau satu kelompok kecil per sesi, selalu berbasis `ARCHITECTURE.md` dan `docs/SCAFFOLD-BLUEPRINT.md`).
2. Setiap OpenCode selesai push ke GitHub, **Hermes Agent (VPS)** menarik perubahan terbaru, menjalankan `bash scripts/verify.sh` di lingkungan Linux bersih, dan melaporkan hasilnya.
3. Jika ada logika Z3 yang macet atau butuh review arsitektur/UI, bawa diff atau trace error ke **Arena.ai** untuk dipecahkan secara presisi.

### Tahap C — Dry Run Menuju NYC (20 Nov)
1. Pastikan seluruh mode `deterministic` berjalan lancar **tanpa internet sekalipun** di laptop yang akan dibawa ke venue NYC.
2. Pastikan `sandbox-agent/AGENTS.md`, `SKILL.md`, dan `hooks/` siap disuntikkan ke Managed Agents saat hari-H.

### Tahap D — Hari-H Hackathon di NYC (21 Nov, 09:00–22:00 EST)
1. Klaim API key/kredit Google DeepMind di venue dan masukkan ke `.env` lokal (jangan pernah push `.env`).
2. Gunakan **OpenCode + Arena.ai** secara bergantian untuk sprint cepat task `PF-019`–`PF-024`:
   * OpenCode menulis adapter `argon_synth.py` & `managed_runner.py`.
   * Arena.ai mengaudit prompt co-generation, skema JSON, dan logika Protected Hooks agar 100% tahan serangan demo.
   * **Hermes Agent (VPS)** memantau backup repo GitHub (push rutin tiap 1–2 jam) dan menjalankan test regresi di VPS sebagai pengaman kedua.

---

## 4. Prompt Siap Pakai untuk Agen Kamu

### 4.1 Prompt untuk Hermes Agent (di VPS LightVela)
Salin prompt ini ke Hermes Agent setelah repo GitHub selesai di-push:

```text
Baca penuh repo `Niumination/proofforge-3d` (`README.md`, `AGENTS.md`, `BACKLOG.md`, `HANDOFF.md`, dan `docs/GITHUB-SETUP.md`).

Tugas kamu sebagai Hermes Agent (LightVela VPS Operator):
1. Clone repo ke workspace proyek terisolasi (mis. `~/projects/proofforge-3d`), terpisah total dari service produksi OpenMausBot/9Router.
2. Pastikan Python >= 3.11 dan Node.js >= 20 tersedia di mesin ini tanpa mengubah service VPS yang sedang berjalan.
3. Jangan membuat file kode aplikasi dulu (status saat ini masih Phase 0 / LOCKED untuk code).
4. Perbarui `BACKLOG.md` (centang PF-003 dan PF-004 jika repo sudah live dan ter-clone bersih) serta catat status kesiapan environment VPS di `HANDOFF.md`, lalu commit & push dengan pesan `docs(pf-004): verify LightVela VPS workspace readiness`.
```

### 4.2 Prompt untuk OpenCode (Saat Kamu Siap Masuk ke Phase 1)
Gunakan prompt ini hanya ketika kamu sudah memberi izin untuk memulai Phase 1:

```text
Baca `AGENTS.md`, `ARCHITECTURE.md`, `BACKLOG.md`, `HANDOFF.md`, dan `docs/SCAFFOLD-BLUEPRINT.md`.
Patuhi semua aturan di `AGENTS.md`: surgical patch, zero warnings, tidak boleh menyimpan secret di repo, dan ikuti kontrak schema di `ARCHITECTURE.md` §4.

Kerjakan Phase 1 secara bertahap dimulai dari branch `feat/pf-005-scaffold` untuk task `PF-005` s.d. `PF-008`:
- Bangun struktur `apps/web`, `apps/api`, `scenarios/`, `sandbox-agent/`, dan `scripts/verify.sh`.
- Gunakan `PROOFFORGE_MODE=deterministic` untuk Phase 1 (belum memanggil API Gemini eksternal).
- Pastikan `scripts/verify.sh` (typecheck + pytest + Z3 smoke test) exit 0 sebelum memperbarui `BACKLOG.md` dan `HANDOFF.md`.
```
