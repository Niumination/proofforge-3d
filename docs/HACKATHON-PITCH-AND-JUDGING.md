# Strategi Judging & Naskah Pitch 2 Menit — ProofForge 3D

Dokumen ini memastikan setiap keputusan teknis yang kita bangun bermuara pada **kemenangan demo 2 menit** di depan juri **Google DeepMind & Cerebral Valley**.

---

## 1. Pemetaan Kriteria Juri

| Kriteria | Apa yang Juri Nilai | Bagaimana ProofForge 3D Membuktikannya Secara Langsung |
| :--- | :--- | :--- |
| **Frontier Capabilities ("Wasn't possible last week")** | Apakah proyek benar-benar memanfaatkan kemampuan baru **Gemini 4 Argon**? | Argon meng-co-generate sistem kontrol, model formal Z3, dan adapter visualisasi 3D secara sinkron—lalu menalar ulang dari *counterexample* matematis. |
| **Visual Coding** | Apakah output visualnya kaya, interaktif, dan informatif? | *3D State-Space Debugger* dengan kamera orbit, *time scrubber*, cincin batas bahaya merah menyala, dan perbandingan *Before vs After*. |
| **Best Use of Managed Agents ($5,000)** | Apakah memakai `antigravity-preview-09-2026` secara esensial (bukan sekadar wrapper)? | Ya: Z3 & simulator berjalan di Linux sandbox terkelola; **Protected Hooks** mencegah agen memalsukan invarian; **Credential Proxy** mengekspor Proof Certificate tanpa membocorkan token. |
| **Technical Rigor & Clarity** | Apakah terlihat nyata dan bebas gimmick? | Setiap transisi `SAT -> Patch -> UNSAT` disertai diff kode riil, hash SHA-256 invarian, dan log solver Z3. |

---

## 2. Koreografi Demo 2 Menit (120 Detik)

> **Aturan Panggung:** Jangan mulai dengan slide panjang atau penjelasan teori Z3. Langsung tampilkan aplikasi berjalan di detik ke-10!

### `0:00 – 0:20` — The Hook (Masalah yang Dirasakan Semua Developer)
* **Visual:** Layar split 3-pane ProofForge 3D sudah terbuka pada skenario *Drone Swarm*.
* **Narasi:**
  *"AI coding agents today write code that looks right and passes basic unit tests—until an edge case hits the physical world and two drones collide. Meet **ProofForge 3D**: a self-verifying compiler and 3D counterexample debugger powered by **Gemini 4 Argon** and **Google Managed Agents**."*

### `0:20 – 0:55` — The Proof & 3D Counterexample Replay (Momen "Aha!")
* **Aksi:** Klik **`Run Verification`** (atau gunakan output run yang baru selesai).
* **Visual:**
  * Panel audit menunjukkan Z3 menemukan **`SAT_VIOLATION`** pada `t = 4.2s` (`v = 14.4 m/s`, `latency = 250ms`).
  * Kanvas 3D memutar gerakan dua drone hingga **berhenti mendadak** pada frame ke-42 dengan dua *safety sphere* berbenturan dan berkedip **MERAH** (`dist = 0.38m < 1.50m`).
* **Narasi:**
  *"Gemini 4 Argon co-generated the control algorithm, a formal Z3 SMT specification, and this 3D adapter. Inside the Managed Agent Linux sandbox, Z3 didn't just guess—it mathematically proved a collision is possible at 4.2 seconds, and we immediately replay that exact failure frame in 3D."*

### `0:55 – 1:30` — Managed Agents, Protected Hooks & Self-Patch (Kunci Hadiah $5K)
* **Aksi:** Tunjukkan **Red-Team Hook Event** & proses *self-patching*.
* **Visual:**
  * Panel kiri/kanan memperlihatkan: saat agen mencoba menyentuh `invariants_locked.py` (atau ketika tombol *"Simulate Reward-Hacking Injection"* dipicu), **Protected Hook** langsung memblokir (`HOOK_BLOCKED: Invariant SHA-256 immutable`).
  * Argon kemudian mengirim **surgical patch** ke `system_impl.py` (diff muncul: penambahan rumus *dynamic stopping distance*).
  * Z3 di sandbox berjalan ulang → lencana berubah hijau: **`UNSAT — PROVEN SAFE`**.
* **Narasi:**
  *"Normally, an autonomous agent might cheat by weakening the safety test. Here, **Managed Agents Protected Hooks** lock our Z3 invariants with an immutable SHA-256 guard. Forced to fix the actual logic, Argon synthesizes a dynamic braking patch, and Z3 proves zero collisions are possible across the entire state space."*

### `1:30 – 2:00` — Before/After 3D Replay & Credential Proxy Export
* **Aksi:** Geser toggle **`Before vs After`**, lalu klik **`Export Proof via Credential Proxy`**.
* **Visual:**
  * Di 3D viewport, pada input ekstrem yang sama (`14.4 m/s`, `250ms`), kedua drone kini melambat dan bermanuver mulus dengan jarak aman `1.62m`.
  * Panel **Proxy Audit** menampilkan ekspor sertifikat bukti ke GitHub melalui **Credential Proxy** dengan token tersensor (`redacted: true`).
* **Narasi:**
  *"Replaying the exact same adversarial parameters now shows clean avoidance, and our **Credential Proxy** publishes the signed proof certificate without ever exposing a real token inside the agent sandbox. That is verifiable autonomous engineering—built today with Gemini 4 Argon and Managed Agents. Thank you."*

---

## 3. Antisipasi Pertanyaan Tajam Juri (Q&A Cheat Sheet)

* **T: Bagaimana kalau model Z3 yang dihasilkan LLM sendiri yang salah?**
  * *Jawab:* Itu sebabnya dalam arsitektur kami **kontrak invarian formal (`invariants_locked.py`) dipisahkan dan dikunci dengan SHA-256 sebelum loop sintesis berjalan**. Agen bebas memperbaiki implementasi dan variabel internal, tetapi tidak pernah boleh mengubah spesifikasi keamanan dasar—dan Protected Hook menegakkan aturan ini di level harness, bukan sekadar di prompt.

* **T: Mengapa ini butuh Gemini 4 Argon, bukan model Flash biasa?**
  * *Jawab:* Co-generation kode sistem + pemodelan simbolik Z3 + adapter trajectory 3D yang konsisten membutuhkan penalaran matematis-spasial panjang sekaligus kesadaran lintas-file dalam satu konteks terpadu. Kami memadukan `gemini-4-argon` untuk sintesis & perbaikan berbasis counterexample, dan `gemini-3.8-flash` / Managed Agents untuk eksekusi verifikasi cepat.

* **T: Apa peran spesifik Managed Agents dibandingkan menjalankan Python lokal biasa?**
  * *Jawab:* Ada tiga alasan inti: (1) isolasi eksekusi kode hasil generasi AI + Z3 solver di Linux sandbox Google yang persisten; (2) **Protected Hooks** yang tidak bisa diedit agen untuk mengunci integritas kontrak formal; dan (3) **Credential Proxy** yang memisahkan token eksternal dari sandbox sehingga *prompt injection* di spesifikasi tidak dapat mencuri kredensial.
