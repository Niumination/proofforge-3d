# ProofForge 3D

> **Self-Verifying Systems Compiler & 3D Visual Counterexample Engine**  
> Built for **Gemini 4 NYC Hackathon** (Cerebral Valley × Google DeepMind — Nov 21, 2026)

[![Target Event](https://img.shields.io/badge/Event-Gemini%204%20NYC%20Hackathon-4285F4)](#)
[![Track](https://img.shields.io/badge/Tracks-Advanced%20Reasoning%20%7C%20Visual%20Coding%20%7C%20Managed%20Agents-34A853)](#)
[![Status](https://img.shields.io/badge/Phase-0%20Documentation%20%26%20Architecture-FBBC05)](#)

---

## 1. Visi & Tesis Utama

AI coding agent saat ini pandai membuat kode yang **"kelihatannya jalan"**, namun sering gagal pada *edge case* fisika, konkurensi, atau batasan keamanan kritis.

**ProofForge 3D** membalik paradigma itu:
1. **Co-Generation (`gemini-4-argon`)**: Dari satu spesifikasi sistem, model menghasilkan tiga artefak terikat secara bersamaan — **(a) kode sistem**, **(b) invarian formal Z3 SMT**, dan **(c) adapter adegan 3D**.
2. **Formal Proof & Counterexample Sandbox (`antigravity-preview-09-2026`)**: Google Managed Agents menjalankan Z3 solver dan property fuzzer di Linux sandbox terkelola. Jika ada celah, Z3 menghasilkan *counterexample trace* konkret.
3. **3D Failure Replay & Surgical Self-Patch**: Antarmuka 3D memutar ulang tepat pada milidetik pelanggaran terjadi (tabrakan drone, torsi sendi robot melewati batas, atau *spatial deadlock*), lalu agen melakukan *surgical patch* pada kode hingga Z3 membuktikan `UNSAT` (100% invariant terpenuhi).
4. **Anti-Cheat Protected Hooks & Credential Proxy**: Agen dilarang memodifikasi atau memperlemah file invarian (dikunci oleh **Protected Hooks** + hash guard), dan integrasi eksternal (seperti ekspor laporan/PR terverifikasi) berjalan lewat **Credential Proxy** tanpa membocorkan token ke konteks agen.

---

## 2. Keselarasan dengan Gemini 4 NYC Hackathon

| Target Hadiah | Bagaimana ProofForge 3D Menjawabnya |
| :--- | :--- |
| **Main Track ($7,500 / $5,000 / $2,500)** | Menggabungkan **Advanced Reasoning** (pembuktian formal Z3 + *counterexample-guided synthesis*), **Visual Coding** (Three.js 3D state-space debugger), dan kapasitas konteks/output panjang **Gemini 4 Argon**. |
| **Best Use of Managed Agents ($5,000)** | Memanfaatkan `antigravity-preview-09-2026` sebagai *verification sandbox* persisten dengan `AGENTS.md`/`SKILL.md`, **Protected Hooks** (mengunci integritas invarian formal), dan **Credential Proxy** (isolasi secret saat publish hasil verifikasi). |

---

## 3. Peta Dokumen Repository (Benang Merah Pembangunan)

Seluruh rancangan dikunci di dokumen berikut sebelum menulis satu baris kode pun:

| Dokumen | Fungsi Utama |
| :--- | :--- |
| [`AGENTS.md`](./AGENTS.md) | Kontrak aturan keras & pembagian peran **Arena.ai**, **Hermes Agent (LightVela VPS)**, **OpenCode**, dan **Gemini 4 Managed Agents**. |
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | Arsitektur teknis 4-lapis, alur data *closed-loop*, kontrak JSON/SSE, model keamanan Hooks & Proxy. |
| [`BACKLOG.md`](./BACKLOG.md) | Peta kerja bertahap (`Phase 0` s.d. `Phase 3`), daftar tugas `PF-001`–`PF-032`, dan *Definition of Done*. |
| [`HANDOFF.md`](./HANDOFF.md) | Papan estafet hidup antar-agen agar pekerjaan tidak bertabrakan saat berpindah dari VPS ke lokal ke lokasi hackathon. |
| [`docs/BRAINSTORMING-AND-DEMO-SCENARIOS.md`](./docs/BRAINSTORMING-AND-DEMO-SCENARIOS.md) | 3 skenario demo 3D yang paling dramatis, *red-team edge cases*, dan matriks fallback. |
| [`docs/SCAFFOLD-BLUEPRINT.md`](./docs/SCAFFOLD-BLUEPRINT.md) | Struktur folder lengkap, fungsi setiap file yang akan dibuat nanti, kebutuhan paket, dan kontrak `.env`. |
| [`docs/MULTI-AGENT-WORKFLOW.md`](./docs/MULTI-AGENT-WORKFLOW.md) | Playbook operasional lintas platform (Arena.ai ↔ Hermes LightVela VPS ↔ OpenCode ↔ Cerebral Valley) beserta prompt handoff siap pakai. |
| [`docs/HACKATHON-PITCH-AND-JUDGING.md`](./docs/HACKATHON-PITCH-AND-JUDGING.md) | Naskah demo 2 menit detik-per-detik dan antisipasi pertanyaan juri Google DeepMind. |
| [`docs/GITHUB-SETUP.md`](./docs/GITHUB-SETUP.md) | Panduan inisialisasi repo GitHub baru (`Niumination/proofforge-3d`) dan sinkronisasi awal ke VPS LightVela. |

---

## 4. Batasan Kepatuhan Hackathon (Pre-Event vs Hari-H)

Untuk menjaga kepatuhan aturan hackathon (*"something built at the hackathon"*):
* **Sebelum 21 Nov 2026 (Phase 0–2):** Hanya menyiapkan dokumentasi, arsitektur, kerangka UI non-AI umum (layout dashboard, viewport Three.js kosong, runner Z3 lokal dasar), serta kesiapan infrastruktur tracking di GitHub & LightVela VPS.
* **Hari-H 21 Nov 2026 (Phase 3):** Klaim kredit API di venue, membangun integrasi inti **Gemini 4 Argon**, konfigurasi **Managed Agents (`antigravity-preview-09-2026`)**, implementasi **Protected Hooks & Credential Proxy**, pengisian 3 skenario pembuktian 3D, pengujian E2E, dan demo final.
