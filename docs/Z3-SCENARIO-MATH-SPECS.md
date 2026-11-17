# Z3 Scenario Math Specs — ProofForge 3D

> **Status:** Pelengkap Phase 0 (Documentation Only — Code Lock tetap LOCKED).
> **Tujuan:** Menghilangkan trial-and-error OpenCode di Batch 1B (PF-009/010/011). Setiap skenario
> punya domain variabel, kontrak invarian formal, rumus bug awal yang *dijamin SAT*, dan rumus fix
> yang *dijamin UNSAT* — lengkap dengan model Z3 yang harus dipakai agar solve < 1 detik.
> **Sumber:** docs/BRAINSTORMING-AND-DEMO-SCENARIOS.md §2 + ARCHITECTURE.md §4. Bila dokumen ini
> berubah, kontrak di SCAFFOLD-BLUEPRINT.md ikut diperbarui (aturan AGENTS.md §2.1).

---

## Konvensi Umum Model Z3 (berlaku untuk 3 skenario)

1. **Solver:** `z3.Solver()` default (QF_LIA / QF_NRA bila perlu trigonometri — lihat Skenario B).
2. **Arithmetic:** gunakan `z3.Real` untuk semua besaran kontinu (hindari Float — lebih lambat & tak deterministik).
3. **Horizon waktu:** diskretisasi `t ∈ [0, T]` dengan tick tetap (T = 10..20 tick per skenario), step `dt` konstan.
4. **Timeout:** `solver.set(timeout=8000)` (8 s) — di bawah gate demo 1.5 s pada tick kecil; bila `unknown` → tampilkan "INCONCLUSIVE", jangan klaim PROVEN SAFE.
5. **Struktur hasil:** setiap run menghasilkan `Counterexample | None`; bila SAT, trace lengkap (nilai variabel per tick) dikirim ke `scene_exporter.py` untuk animasi 3D.
6. **Uji kontrak wajib (unit test PF-009..011):**
   - `test_buggy_is_sat`: model buggy → SAT dengan counterexample di nilai yang diharapkan.
   - `test_fixed_is_unsat`: model fixed → UNSAT pada domain penuh.
   - Keduanya deterministik (tanpa random seed) — nilai counterexample di-assert persis.

---

## Skenario A — drone_swarm (HERO DEMO)

### Domain variabel (semua `Real`)

| Variabel | Range | Catatan |
|---|---|---|
| `v_A`, `v_B` | [10, 15] m/s | kecepatan konstan drone A & B |
| `latency` | [0.05, 0.30] s | sensor + braking latency (nilai sama utk kedua drone) |
| `heading_A`, `heading_B` | sudut konstanta (fixed per counterexample demo) | lintasan lurus berpotongan; gunakan heading 90° & 0° agar persamaan linier |
| `t` | [0, 10] s, tick `dt = 0.1` | horizon 10 s |
| `a_max` | konstanta 3.0 m/s² | batas deselerasi |
| `R_safe` | konstanta **1.50 m** | TERKUNCI di `invariants_locked.py` |

### Kontrak invarian (locked)
Untuk semua tick `k`: `‖p_A(k·dt) − p_B(k·dt)‖₂ ≥ R_safe`.

### Rumus posisi (linier, terkalibrasi numerik)
- Drone **head-on** dengan offset lateral kecil: A bergerak arah +Y, B arah +Y juga (menyusul/berpapasan sejajar).
  `p_A(t) = (0, v_A·t − v_A·t₀)`, `p_B(t) = (0.38, −v_B·t₀ + v_B·t)` — offset lateral `0.38 m` tetap.
- **Kalibrasi terbukti (dihitung Python):** dengan `t₀ = 4.2`, `d₀ = v_B·t₀ = 58.38 m`, `v_A = 14.4`,
  `v_B = 13.9` → jarak minimum = **0.38 m pada t ≈ 4.17 s**, dan 0.43 m pada t=3.8 & t=4.6
  (jadi pelanggaran benar-benar terkonsentrasi sempit — pas untuk freeze-frame).
- **Model buggy** (ini bugnya): kontroler menganggap aman bila `dist_now ≥ R_safe − v·latency`
  (kompensasi latensi *naive* — hanya mengurangi satu suku, tidak memperhitungkan jarak pengereman inersia `v²/(2·a_max)`).
  Dengan `R_safe − v_A·latency = 1.50 − 3.6 = −2.1` → syarat selalu "terpenuhi", bug tidak pernah terdeteksi
  oleh tes biasa. **Assert test: `sat == True` dan `min_dist < 0.5`.**

### Counterexample target (SAT) — nilai untuk demo
`v_A = 14.4`, `v_B = 13.9`, `latency = 0.25` → jarak minimum **0.38 m < 1.50 m** pada `t ≈ 4.2 s`
(geometri lintasan & kalibrasi lengkap: lihat "Rumus posisi" di atas — dihitung & diverifikasi numerik).

### Rumus fix (UNSAT) — *dynamic stopping-envelope braking*
Ganti syarat kontroler menjadi:
```
required_gap(t) = R_safe + (v_A + v_B)·latency + (v_A² + v_B²)/(2·a_max)
```
dan kontroler *wajib* mulai braking saat `‖p_A − p_B‖ ≤ required_gap(t)`. Dalam model Z3 fixed,
posisi dikonstrainkan oleh profil braking (v berkurang linier dengan a_max setelah trigger), sehingga
untuk seluruh domain `[10,15]² × [0.05,0.30]` invarian locked terpenuhi → **UNSAT**.
- Batasi horizon: dengan v_max 15 dan a_max 3.0, jarak berhenti maks ≈ 15·0.30 + 15²/6 ≈ 42 m;
  titik potong origin dengan spawn ≥ 150 m memastikan braking selesai sebelum bertemu — tak pernah UNSAT gagal.

### Catatan scene_adapter
- Output per tick: posisi (x,y,z≈0), radius safety sphere = `R_safe`, warna merah bila `dist < R_safe`.
- Counterexample demo: zoom kamera otomatis pada tick `violated_tick = round(4.2/dt) = 42`.

---

## Skenario B — robot_arm (3-DOF Torque & Joint Envelope)

### Domain variabel

| Variabel | Range | Catatan |
|---|---|---|
| `θ1, θ2, θ3` | shoulder [−90°, 90°], elbow [−120°, 120°], wrist [−90°, 90°] | sudut sendi (dalam radian di Z3) |
| `target` | (x,y) ∈ boundary workspace | beban pada target akhir |
| `L1, L2, L3` | konstanta 0.35, 0.30, 0.12 m | panjang segmen |
| `τ_max` | konstanta 8.0 N·m | batas torsi |
| `m_payload` | [0.5, 5.0] kg | beban |
| `g` | 9.81 | gravitasi |

### Kontrak invarian (locked)
1. `θk ∈ [θk_min, θk_max]` untuk semua sendi.
2. `|τk| ≤ τ_max` untuk semua sendi.
3. Effector `y ≥ 0.15 m` (zona terlarang meja).

### Linearisasi trig (KRITIS — anti Z3 timeout)
Model kinematika penuh memakai sin/cos non-linier (`QF_NRA`) berisiko hang. Gunakan **linearisasi
per-tick di sekitar sudut nominal** yang dihitung Python (bukan di Z3):
- `sin(θ) ≈ sin(θ_nom) + cos(θ_nom)·(θ − θ_nom)`, `cos(θ) ≈ cos(θ_nom) − sin(θ_nom)·(θ − θ_nom)`
- Set `θ_nom` = solusi IK numerik dari target (dihitung Python + numpy); Z3 hanya mencari deviasi
  `δ = θ − θ_nom` dalam [−0.2, 0.2] rad yang melanggar invarian. Model menjadi **QF_LIA murni**.

### Torsi (model linier)
`τ2 ≈ (m_payload·g·L2_eff)·|cos(θ2_nom)| + m_link2·g·L2_c·|cos(θ2_nom)|` — dengan `L2_eff` jarak
effector ke sendi elbow. Suku dinamis (Coriolis) diabaikan — gerakan quasi-statik, cukup untuk demo.

### Rumus bug (SAT)
IK buggy **tidak meng-clamp dekat singularitas**: saat `‖target‖ → L1+L2+L3` (boundary workspace),
Jacobian mendekati singular, dan model membiarkan `|δ|` bebas hingga 0.2 rad. Ambil target
`x = 0.70, y = 0.20, m_payload = 4.5` → `τ2 ≈ 4.5·9.81·0.35 ≈ 15.4 N·m > 8.0` → **SAT**
(counterexample: elbow pada boundary). Assert test: `tau2 > 8.0` pada model buggy.

### Rumus fix (UNSAT)
Tambahkan di kontroler (bukan di invariants!):
1. **Clamp workspace:** hanya terima target dengan `‖target‖ ≤ 0.9·(L1+L2+L3)`.
2. **Clamp payload:** `m_payload ≤ τ_max / (g·L2_eff·|cos(θ2_nom)|)`.
Z3 fixed mengecek seluruh domain yang lolos kedua clamp → tak ada `δ` yang melanggar → **UNSAT**.

### Catatan scene_adapter
- Forward-kinematics 3 joint (Python) per tick → posisi segmen untuk Three.js primitives.
- Warna sendi merah bila `|τk| > 0.9·τ_max` (peringatan) / `> τ_max` (pelanggaran, freeze-frame).

---

## Skenario C — spatial_tiling (Grid 3D Deadlock)

### Domain variabel

| Variabel | Range | Catatan |
|---|---|---|
| `workers` | W = 4 konstanta | agen pekerja |
| `grid` | 4×4×4 sel (x,y,z ∈ [0,3]) | target path masing-masing worker ditetapkan deterministik |
| `tick` | [0, 20] | horizon 20 tick |
| `pos_w(t)`, `hold_w(t)` | sel integer | posisi & sel yang di-hold (Int di Z3) |

### Kontrak invarian (locked)
1. **Mutual exclusion:** `∀ w≠w', ∀t: ¬(hold_w(t) = hold_w'(t))` (sel hold unik per tick).
2. **Deadlock-freedom:** tidak ada siklus tunggu `w1→w2→…→w1` yang bertahan > 3 tick berturut.

### Encoding deadlock-freedom di Z3
- State tunggu: `waiting(w,t) = (pos_w(t) ≠ goal_w) ∧ (sel tujuan sedang di-hold worker lain)`.
- Siklus: cukup deteksi **pairwise circular wait** (w1 tunggu sel milik w2 DAN w2 tunggu sel milik w1
  pada tick yang sama, ≥ 4 tick berturut) — versi ring penuh tak perlu untuk grid 4×4×4 4-worker
  (deadlock minimal selalu pasangan; tulis asumsi ini di komentar spec.md).
- Semua variabel `Int` → QF_LIA murni, solve < 0.5 s.

### Rumus bug (SAT)
Lock acquisition **tanpa urutan kanonik**: worker mengunci sel tujuan dulu, baru sel transit.
Counterexample deterministik: W1 di (0,0,0) menuju (1,0,0); W2 di (1,0,0) menuju (0,0,0); keduanya
hold sel transit lawan pada tick 18 (nilai demo sesuai BRAINSTORMING: `DEADLOCK DETECTED at tick 18`).
Assert test: `pairwise_wait_length ≥ 4` pada tick 18, `sat == True`.

### Rumus fix (UNSAT) — *canonical lock ordering*
Semua worker **wajib** mengunci sel dalam urutan total global: `sort(key = (x, y, z, worker_id))`.
Implementasi di kontroler: sebelum mengunci, tukar urutan jika `sel_tujuan < sel_transit` secara
lexicographic. Z3 fixed membuktikan: karena semua mengikuti urutan total, siklus tunggu mustahil →
**UNSAT** pada horizon penuh 20 tick.

### Catatan scene_adapter
- Render kubus grid 3D, panah ketergantungan merah antar worker yang saling tunggu.
- `violated_tick = 18` untuk freeze-frame demo.

---

## Ringkasan Kontrak Uji (untuk verify.sh / pytest Batch 1B)

| Skenario | test_buggy | test_fixed | Solver | Budget |
|---|---|---|---|---|
| drone_swarm | SAT, min_dist < 0.5 m | UNSAT | QF_LIA | < 1 s |
| robot_arm | SAT, τ2 > 8.0 | UNSAT | QF_LIA (linearisasi per-tick) | < 1 s |
| spatial_tiling | SAT, deadlock @ tick 18 | UNSAT | QF_LIA (Int) | < 0.5 s |

**Aturan emas:** invariants_locked.py hanya berisi kontrak (tabel di atas) — rumus bug & fix hidup
di `buggy_impl.py` / kontroler, BUKAN di invariants. SHA-256 invariants dihitung sekali oleh
`invariant_guard.py` sebelum run pertama.
