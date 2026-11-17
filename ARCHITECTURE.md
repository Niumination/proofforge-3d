# ARCHITECTURE.md — Arsitektur Teknis ProofForge 3D

Dokumen ini mendefinisikan arsitektur teknis lengkap, kontrak data, dan mekanisme keamanan **ProofForge 3D**.

---

## 1. Diagram Arsitektur Sistem (High-Level)

```
┌───────────────────────────────────────────────────────────────────────────┐
│                  FRONTEND COCKPIT (React 19 + TypeScript)                 │
│  ┌─────────────────┐  ┌─────────────────────────┐  ┌───────────────────┐  │
│  │ Spec & Scenario │  │  3D State-Space Viewer  │  │  Proof & Security │  │
│  │    Composer     │  │   (Three.js / R3F)      │  │   Audit Console   │  │
│  │                 │  │                         │  │                   │  │
│  │ • Preset / Text │  │ • Time Scrubber [0..T]  │  │ • Z3 SAT/UNSAT    │  │
│  │ • Locked        │  │ • Red Failure Frame     │  │ • Protected Hooks │  │
│  │   Invariants    │  │ • Before/After Toggle   │  │ • Credential Proxy│  │
│  │ • Voice (Live)  │  │ • Vector/Force Overlay  │  │ • Patch Diff Log  │  │
│  └────────┬────────┘  └────────────▲────────────┘  └─────────▲─────────┘  │
└───────────┼────────────────────────┼─────────────────────────┼────────────┘
            │ POST /api/forge/run    │ SSE /api/forge/stream/:id
            ▼                        │
┌───────────────────────────────────────────────────────────────────────────┐
│                ORCHESTRATOR API (Python FastAPI + SSE)                    │
│                                                                           │
│  1. Lock Invariants (SHA-256)     3. Stream Counterexample Frames         │
│  2. Call Gemini Interactions API  4. Manage Iteration Budget (max N=5)    │
└───────────┬────────────────────────────────────────────┬──────────────────┘
            │                                            │
            ▼                                            ▼
┌───────────────────────────────┐        ┌──────────────────────────────────┐
│   GEMINI 4 ARGON              │        │   GOOGLE MANAGED AGENTS          │
│   (gemini-4-argon)            │        │   (antigravity-preview-09-2026)  │
│                               │        │                                  │
│ • Co-Generate:                │        │ • Ephemeral Linux Sandbox        │
│   1. system_impl.py           │◄──────►│ • Executes Z3 Solver & Fuzzer    │
│   2. z3_verifier.py           │ Patch  │ • Protected Hooks:               │
│   3. scene_adapter.py         │  Loop  │   - Immutable invariant hash     │
│ • Spatial & Mathematical      │        │   - Forbidden syscall/network    │
│   Reasoning                   │        │ • Credential Proxy:              │
│ • Patch Synthesis from        │        │   - Domain-scoped secret swap    │
│   Counterexample Trace        │        │     (e.g., GitHub PR export)     │
└───────────────────────────────┘        └──────────────────────────────────┘
```

---

## 2. Alur Eksekusi Closed-Loop (Step-by-Step)

1. **Tahap 1 — Input & Penguncian Kontrak (`LOCK_INVARIANTS`)**
   * Pengguna memilih skenario (mis. *Drone Swarm Collision*, *Robot Arm Torque Envelope*, *Distributed Spatial Tiling*) atau menulis spesifikasi baru.
   * Sistem menampilkan **Invarian Formal** (aturan matematika yang tidak boleh dilanggar) dan menghitung **SHA-256 digest** atas kontrak invarian tersebut.
   * Jika mode *Showcase Bug* aktif, sistem memulai dari implementasi awal yang mengandung bug halus (*realistic edge-case bug*).

2. **Tahap 2 — Co-Generation (`SYNTHESIZE_ARTIFACTS`)**
   * Orchestrator memanggil `gemini-4-argon` untuk menghasilkan atau memetakan tiga komponen dalam skema terstruktur:
     * **System Code** (`system_impl.py`): Logika kontrol/algoritma target.
     * **Z3 Proof Harness** (`z3_harness.py`): Pemodelan simbolik atas state sistem yang mengimpor invarian terkunci.
     * **3D Trajectory Exporter** (`scene_adapter.py`): Mengekstrak jejak koordinat, orientasi, batas zona aman, dan vektor gaya per *tick* waktu `t = 0..T` menjadi JSON frame 3D.

3. **Tahap 3 — Eksekusi Pembuktian di Managed Agents (`VERIFY_IN_SANDBOX`)**
   * Orchestrator mengirim artefak ke **Managed Agent (`antigravity-preview-09-2026`)** dengan konfigurasi `AGENTS.md`, `SKILL.md`, dan **Protected Hooks**.
   * Di dalam Linux sandbox terisolasi, agen menjalankan `python3 z3_harness.py`.
   * **Cabang A — `SAT` (Ditemukan Counterexample / Bug Terbukti!):**
     * Z3 menemukan penugasan variabel konkret (mis. `v_drone1 = 12.4 m/s`, `dt = 0.2s`, `dist = 0.08m < R_safe`).
     * `scene_adapter.py` memutar simulasi tepat dengan input *counterexample* tersebut dan menghasilkan `counterexample_frames.json` beserta `violated_frame_index` & `violated_invariant`.
     * Frontend langsung memutar animasi 3D hingga berhenti dan berkedip merah tepat pada frame pelanggaran!
   * **Cabang B — `UNSAT` (Terbukti Aman Secara Matematis!):**
     * Z3 membuktikan tidak ada kombinasi input dalam domain yang dapat melanggar invarian.
     * Protected Hook memvalidasi ulang bahwa SHA-256 `invariants_locked.py` identik dengan nilai awal.
     * Sistem menandai status `PROVEN_SAFE` dan menampilkan simulasi 3D bersih + perbandingan *Before vs After*.

4. **Tahap 4 — Surgical Self-Patch Loop (`PATCH_AND_REVERIFY`)**
   * Saat status `SAT`, trace *counterexample* dan diagnosa matematis dikirim kembali ke `gemini-4-argon` (atau Managed Agent dengan budget iterasi maksimal `N = 5`).
   * Agen menghasilkan **unified diff** (*surgical patch*) hanya pada `system_impl.py`, lalu mengulang Tahap 3.
   * Setiap iterasi tercatat di timeline UI (`Iteration #1: SAT at t=4.2s` → `Patch Applied` → `Iteration #2: UNSAT / PROVEN SAFE`).

5. **Tahap 5 — Verified Artifact Export via Credential Proxy (`SECURE_PUBLISH`)**
   * *(Demo unggulan untuk kategori Managed Agents)*: Setelah status `PROVEN_SAFE`, pengguna bisa menekan **"Export Proof Certificate / Open Verified PR"**.
   * Sandbox Managed Agent memanggil endpoint GitHub/webhook melalui **Credential Proxy**—di dalam sandbox agen hanya melihat dummy token `PROXY_MANAGED_GITHUB_TOKEN`, sementara proxy luar menukar token asli **hanya** untuk domain `api.github.com` yang diizinkan.

---

## 3. Arsitektur Keamanan & Protected Hooks

| Lapisan | Mekanisme | Tujuan Demo ke Juri DeepMind |
| :--- | :--- | :--- |
| **1. Invariant Immutability Hook** | Membandingkan hash SHA-256 `invariants_locked.py` sebelum & sesudah eksekusi agen. | Mencegah agen "berbuat curang" dengan menghapus/melonggarkan aturan pembuktian Z3. |
| **2. Patch Scope Guard Hook** | Menolak `write_to_file` / patch jika menyentuh direktori selain `workspace/impl/` dan `workspace/skills/`. | Membuktikan agen tidak dapat memodifikasi harness verifier atau file hook itu sendiri. |
| **3. Credential Proxy** | Secret disimpan *write-only* di luar sandbox; injeksi secret hanya terjadi di egress proxy untuk domain `allowlist`. | Membuktikan *prompt injection* di dalam kode/spesifikasi target tidak bisa mencuri API key atau GitHub token. |
| **4. Iteration & Token Budget** | `max_iterations = 5`, timeout eksekusi Z3 per pass = `15s`. | Mencegah *infinite loop* saat hackathon demo dan menjaga latensi demo tetap di bawah ~30 detik. |

---

## 4. Kontrak Data Utama (Schema Specification)

> *Catatan: Ini adalah spesifikasi desain kontrak JSON sebelum implementasi TypeScript & Pydantic dilakukan pada fase coding.*

### 4.1 `ForgeRunRequest`
```json
{
  "scenario_id": "drone-swarm-v1",
  "mode": "live_gemini | deterministic_fallback",
  "custom_spec": "Optional natural language override",
  "inject_initial_bug": true,
  "max_iterations": 5,
  "enable_adversarial_hook_test": false
}
```

### 4.2 `VerificationResult`
```json
{
  "iteration": 1,
  "status": "SAT_VIOLATION | UNSAT_PROVEN | ERROR",
  "invariant_hash_valid": true,
  "violated_invariant": "min_pairwise_distance >= 1.50m",
  "counterexample_inputs": {
    "drone_a_speed": 14.2,
    "drone_b_speed": 13.8,
    "comm_delay_ms": 240
  },
  "violated_tick": 42,
  "violated_time_sec": 4.2,
  "solver_duration_ms": 184
}
```

### 4.3 `SceneTimelineFrame` (Untuk Three.js / R3F)
```json
{
  "tick": 42,
  "time_sec": 4.2,
  "is_violation": true,
  "entities": [
    {
      "id": "drone-alpha",
      "kind": "quadrotor",
      "position": [1.24, 3.0, -0.45],
      "rotation_euler": [0.12, 0.0, -0.25],
      "velocity": [14.2, 0.0, 0.0],
      "status": "COLLISION"
    }
  ],
  "constraints_overlay": [
    {
      "type": "safety_sphere",
      "center": [1.24, 3.0, -0.45],
      "radius": 1.5,
      "breached": true
    }
  ]
}
```

### 4.4 `SSEStreamEvent` (Real-time Telemetry ke Frontend)
Event types yang mengalir lewat `GET /api/forge/stream/{run_id}`:
* `STAGE_CHANGED` (`LOCK_INVARIANTS`, `SYNTHESIZE`, `VERIFY`, `PATCH`, `COMPLETE`)
* `AGENT_LOG` (streaming reasoning summary & tool execution dari Managed Agent)
* `HOOK_AUDIT` (`ALLOW` / `BLOCKED` beserta alasan & hash check)
* `PROXY_AUDIT` (`domain`, `credential_ref`, `redacted: true`, `status_code`)
* `VERIFICATION_RESULT` (payload `VerificationResult` + `SceneTimelineFrame[]`)
* `PATCH_DIFF` (unified diff + penjelasan perubahan matematis)

---

## 5. Pemilihan Stack & Justifikasi Teknis

| Komponen | Teknologi Pilihan | Alasan Pemilihan (Sesuai Skill Set Niumination) |
| :--- | :--- | :--- |
| **Frontend Cockpit** | **Vite 7 + React 19 + TypeScript 5.7 + Tailwind v4** | Cepat untuk iterasi 12 jam hackathon, identik dengan stack `Flame-ADE` & `Niu-Humanoid`. |
| **3D Engine** | **Three.js (`@react-three/fiber` + `@react-three/drei`)** | Ringan di browser, mendukung kamera orbit, shader glow untuk *violation sphere*, dan timeline scrubbing 60 FPS. |
| **State & Diff UI** | **Zustand 5 + diff viewer ringan** | Konsisten dengan arsitektur store `Flame-ADE` (`chatStore`, `approvalStore`). |
| **Backend Orchestrator** | **Python 3.11+ + FastAPI + SSE (`sse-starlette`)** | Ekosistem resmi **Z3 (`z3-solver`)** dan SDK resmi **`google-genai` (Interactions API / Managed Agents)** paling matang di Python. |
| **Formal Solver** | **`z3-solver` (Microsoft Research)** | Standar industri SMT solver; mampu membuktikan pertidaksamaan kinematika, batas torsi, dan deadlock dalam hitungan milidetik. |
| **AI & Sandbox** | **`gemini-4-argon` + `antigravity-preview-09-2026` + `gemini-3.8-flash`** | Kombinasi wajib hackathon untuk reasoning panjang, sub-agen cepat, dan eksekusi sandbox terkelola. |
| **Optional Voice** | **`gemini-3.8-live`** *(Stretch goal di Phase 3)* | Memungkinkan juri menyuntikkan constraint baru lewat suara saat demo live. |
