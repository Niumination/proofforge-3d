# AGENTS.md — Multi-Agent Engineering Contract (ProofForge 3D)

Dokumen ini adalah **aturan tertinggi** bagi seluruh agen AI dan operator manusia yang bekerja pada repositori `proofforge-3d`.

---

## 1. Tim Agen & Pembagian Tugas Mutlak

| Agen / Platform | Peran Resmi | Tanggung Jawab Utama | Batasan Tegas (DILARANG) |
| :--- | :--- | :--- | :--- |
| **Arena.ai** | *Chief Architect & Deep Reviewer* | Desain arsitektur, spesifikasi kontrak data, audit kualitas kode/keamanan, perumusan skenario Z3 yang kompleks, dan penyusunan naskah pitch. | Tidak langsung men-deploy ke VPS produksi tanpa review; tidak menebak isi file yang tidak dibaca. |
| **Hermes Agent** *(LightVela VPS)* | *24/7 Cloud Operator & Verification Gatekeeper* | Sinkronisasi repo GitHub di VPS LightVela, menjalankan `scripts/verify.sh` / test suite, menjaga state `BACKLOG.md` & `HANDOFF.md`, mengelola staging preview via Cloudflare Tunnel (`--protocol http2`). | **DILARANG** menulis atau mengubah file tanpa membaca `HANDOFF.md`; **DILARANG** meng-commit `.env`, API key, token Telegram/OMB, atau file runtime. |
| **OpenCode** | *Interactive Surgical Coder* | Implementasi kode tahap demi tahap (`apps/web`, `apps/api`, `sandbox-agent`) secara lokal/terarah sesuai task ID di `BACKLOG.md`, menjalankan typecheck & unit test sebelum commit. | **DILARANG** melakukan rewrite massal di luar scope task ID aktif; wajib menjaga zero warnings/errors. |
| **Gemini 4 Argon + Managed Agents** *(Target Runtime)* | *In-App Verification & Synthesis Engine* | Menghasilkan kode + invarian Z3 + adegan 3D, mengeksekusi pembuktian di sandbox Linux Google, serta melakukan *self-patching* di bawah pengawasan Protected Hooks. | **DILARANG** mengubah atau melemahkan isi `invariants.py` (diblokir oleh Protected Hooks + SHA-256 hash check). |

---

## 2. Prinsip Rekayasa Inti (Niumination Standard)

1. **Documentation First, Code Second:** Tidak ada modul aplikasi yang ditulis sebelum kontraknya ada di `ARCHITECTURE.md` dan terdaftar di `BACKLOG.md`.
2. **Surgical Patch, Zero Redundancy:** Ubah hanya bagian yang diperlukan oleh task ID aktif (mis. `[PF-012]`). Hindari duplikasi helper, CSS, atau tipe data.
3. **Proof Before Claim:** Setiap klaim *"selesai"* di `BACKLOG.md` atau `HANDOFF.md` wajib menyertakan bukti perintah uji yang benar-benar dijalankan (exit code `0`).
4. **Everything Is Verifiable:** Tidak ada rahasia di Git. Semua kredensial menggunakan `.env.example` sebagai kontrak dan `.env` lokal/Managed Credential Proxy saat runtime.
5. **Single-Command Handoff:** Setiap pergantian agen (mis. dari OpenCode ke Hermes VPS atau sebaliknya) wajib memperbarui `HANDOFF.md` dengan format ringkas: *What Changed → Tests Passed → Next Task ID → Blockers*.

---

## 3. Aturan Keamanan & Jaringan (Khusus Ekosistem LightVela VPS)

Mengacu pada standar operasional ekosistem **LightVela (`zbmaus-vela` / `mirai`)**:
* Service internal/staging pada VPS harus mematuhi konfigurasi tunnel aman; jika diekspos lewat `cloudflared`, wajib memakai `--protocol http2` agar payload besar/SSE tidak hang atau 502.
* Jangan pernah meletakkan token Gemini, GitHub PAT, atau kunci 9Router/OMB ke dalam repositori Git atau prompt log yang di-commit.
* Isolasi workspace proyek `proofforge-3d` di folder terpisah dari service produksi OMB/9Router agar tidak mengganggu bot aktif di VPS.

---

## 4. Konvensi Git & Branching

* `main`: Selalu dalam keadaan bersih, terdokumentasi, dan lolos verifikasi.
* `docs/*`: Perubahan arsitektur, backlog, atau skenario demo.
* `feat/pf-XXX-<slug>`: Branch pengerjaan kode per task ID (mis. `feat/pf-008-z3-runner`).
* Format commit: `<type>(pf-XXX): <ringkasan singkat>` (contoh: `docs(pf-001): finalize architecture and workflow specs`).

---

## 5. Aturan Emas Invarian (Khusus Domain ProofForge 3D)

Dalam aplikasi **ProofForge 3D**, masalah terbesar sistem AI *self-healing* adalah **reward hacking** (agen menghapus atau melonggarkan assertion agar tes terlihat lulus). Oleh karena itu:
* File kontrak invarian (`invariants_locked.py`) di-hash dengan **SHA-256** sebelum loop perbaikan dimulai.
* **Protected Hook** di Managed Agents memeriksa hash tersebut sebelum setiap langkah verifikasi dan sebelum deklarasi `PROVEN SAFE`.
* Jika agen mencoba menyentuh `invariants_locked.py`, hook menolak aksi tersebut, mencatat event `HOOK_BLOCKED_INVARIANT_TAMPER`, dan menampilkannya secara transparan di panel audit UI.
