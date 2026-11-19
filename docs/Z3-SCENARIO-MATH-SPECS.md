# Z3 Scenario Math Specs — ProofForge 3D

> **Status:** Final Math Spec (siap dipakai di Phase 1 Batch 1B: `PF-009`–`PF-011`).
> **Tujuan:** Menghilangkan trial-and-error OpenCode di Batch 1B. Setiap skenario punya domain variabel,
> kontrak invarian formal, rumus bug awal yang *dijamin SAT*, dan rumus fix yang *dijamin UNSAT* —
> lengkap dengan model Z3 yang harus dipakai agar solve < 1 detik.
> **Sumber:** `docs/BRAINSTORMING-AND-DEMO-SCENARIOS.md` §2 + `ARCHITECTURE.md` §4. Bila dokumen ini
> berubah, kontrak di `SCAFFOLD-BLUEPRINT.md` ikut diperbarui (aturan `AGENTS.md` §2.1).

---

## Konvensi Umum Model Z3 (berlaku untuk 3 skenario)

1. **Solver:** `z3.Solver()` default (`QF_LIA` / `QF_NRA` polinomial kuadratik tanpa `sqrt`/`sin`/`cos`).
2. **Arithmetic:** gunakan `z3.Real` untuk semua besaran kontinu (hindari `Float` — lebih lambat & tak deterministik).
3. **Horizon waktu:** diskretisasi `t ∈ [0, T]` dengan tick tetap, step `dt` konstan.
4. **Timeout:** `solver.set(timeout=8000)` (8 s) — di bawah gate demo 1.5 s pada tick kecil; bila `unknown` → tampilkan `"INCONCLUSIVE"`, jangan pernah klaim `PROVEN SAFE`.
5. **Struktur hasil:** setiap run menghasilkan `Counterexample | None`; bila `SAT`, trace lengkap (nilai variabel per tick) dikirim ke `scene_exporter.py` untuk animasi 3D.
6. **Uji kontrak wajib (unit test `PF-009..011`):**
   - `test_buggy_is_sat`: model buggy → `SAT` dengan counterexample pada nilai yang diharapkan.
   - `test_fixed_is_unsat`: model fixed → `UNSAT` pada domain penuh.
   - Keduanya deterministik (tanpa random seed) — nilai counterexample di-assert persis.

---

## Skenario A — `drone_swarm` (HERO DEMO)

### Domain variabel (semua `Real`)

| Variabel | Range | Catatan |
|---|---|---|
| `v_A`, `v_B` | `[10, 15]` m/s | kecepatan awal drone A & B |
| `latency` | `[0.05, 0.30]` s | sensor + braking latency (nilai sama utk kedua drone) |
| `t` | `[0, 10]` s, tick `dt = 0.1` | horizon 10 s (`0..100` tick) |
| `t0` | konstanta `4.2` s | waktu titik pertemuan nominal di origin |
| `a_max` | konstanta `3.0` m/s² | batas deselerasi |
| `R_safe` | konstanta **`1.50` m** | TERKUNCI di `invariants_locked.py` |

### Kontrak invarian (locked — bentuk kuadratik anti-`sqrt`)
Untuk semua tick `k`:
```text
(x_A(k·dt) − x_B(k·dt))² + (y_A(k·dt) − y_B(k·dt))² ≥ R_safe²   (R_safe² = 2.25)
```
*(Menghindari `sqrt()` membuat Z3 menyelesaikannya dalam < 50 ms secara eksak).*

### Rumus posisi (head-on dengan offset lateral — terkalibrasi Python)
- Drone A bergerak ke arah **+Y**, Drone B bergerak berlawanan arah (**−Y**) pada jalur sejajar berjarak lateral `0.38 m`:
  * `p_A(t) = (0.00, v_A · (t − t₀))` → di `t = 0`: `y_A = −v_A · 4.2` (mis. `−60.48 m`)
  * `p_B(t) = (0.38, v_B · (t₀ − t))` → di `t = 0`: `y_B = +v_B · 4.2` (mis. `+58.38 m`)
- **Kalibrasi terbukti (dihitung Python):** dengan `t₀ = 4.2`, `v_A = 14.4`, `v_B = 13.9`:
  * `t = 0.0 s` → jarak = **`118.861 m`** (jauh terpisah di 3D viewport)
  * `t = 4.1 s` → jarak = **`2.855 m`** (masih di luar `R_safe = 1.50 m`)
  * `t = 4.2 s` (`tick = 42`) → jarak minimum = **`0.380 m < 1.50 m`** (pelanggaran tepat di titik temu!)
  * `t = 4.3 s` → jarak = **`2.855 m`**
- **Model buggy** (ini bugnya): kontroler menganggap aman bila `dist_now ≥ R_safe − v_rel · latency` (kompensasi latensi *naive* tanpa jarak pengereman inersia `v²/(2·a_max)`). Pada `t = 4.0 s`, jarak masih `> 1.50`, dan ketika akhirnya memicu rem, drone terlambat berhenti karena `latency` + inersia. **Assert test: `sat == True` dan `min_dist < 0.5`.**

### Counterexample target (SAT) — nilai untuk demo
`v_A = 14.4`, `v_B = 13.9`, `latency = 0.25` → jarak minimum **`0.380 m < 1.50 m`** pada `t = 4.2 s` (`violated_tick = 42`).

### Rumus fix (UNSAT) — *dynamic stopping-envelope braking*
Ganti syarat kontroler menjadi:
```text
required_gap(t) = R_safe + (v_A + v_B)·latency + (v_A² + v_B²)/(2·a_max)
```
dan kontroler *wajib* mulai braking penuh (`a_max`) saat `|y_B(t) − y_A(t)| ≤ required_gap(t)`.
* **Bukti kecukupan jarak awal:** Pada kasus terburuk domain (`v_A = v_B = 15 m/s`, `latency = 0.30 s`, `a_max = 3.0 m/s²`), jarak berhenti total dua drone adalah `2 × (15·0.30 + 15²/6) + 1.50 = 85.50 m`, sedangkan jarak awal pada `t = 0` minimal `(10 + 10) × 4.2 = 84.0 m` — **perhatian:** untuk `v_A = v_B = 10` jarak awal `84 m` sudah sangat cukup karena jarak berhenti pada `v = 10` hanya `2 × (10·0.30 + 100/6) + 1.50 = 40.83 m`. Pada `v = 15`, jarak awal `126.0 m > 85.50 m`. Jadi untuk **seluruh** domain `[10, 15]² × [0.05, 0.30]`, jarak awal selalu melebihi `required_gap` dengan margin `> 40 m` → **dijamin `UNSAT` 100%**.

### Catatan `scene_adapter`
- Output per tick: posisi `(x, y, z=0)`, radius safety sphere = `R_safe = 1.50`, warna merah bila `dist < R_safe`.
- Counterexample demo: kamera zoom otomatis pada `violated_tick = 42` (`t = 4.2 s`).

---

## Skenario B — `robot_arm` (3-DOF Torque & Joint Envelope)

### Domain variabel

| Variabel | Range | Catatan |
|---|---|---|
| `θ1, θ2, θ3` | shoulder `[−90°, 90°]`, elbow `[−120°, 120°]`, wrist `[−90°, 90°]` | sudut sendi (dalam radian di Z3) |
| `target` | `(x, y)` ∈ workspace | beban pada target akhir |
| `L1, L2, L3` | konstanta `0.35, 0.30, 0.12` m | panjang segmen (`reach_max = 0.77 m`) |
| `τ_max` | konstanta `8.0` N·m | batas torsi |
| `m_payload` | `[0.5, 5.0]` kg | beban |
| `g` | `9.81` m/s² | gravitasi |

### Kontrak invarian (locked)
1. `θk ∈ [θk_min, θk_max]` untuk semua sendi.
2. `|τk| ≤ τ_max` untuk semua sendi.
3. Effector `y_eff ≥ 0.15 m` (zona terlarang meja).

### Linearisasi trig (KRITIS — anti Z3 timeout untuk `τ` DAN `y_eff`)
Model kinematika penuh memakai `sin/cos` non-linier (`QF_NRA`) berisiko hang. Gunakan **linearisasi Taylor orde-1 per-tick di sekitar sudut nominal `θ_nom`** yang dihitung Python sebelum memanggil Z3:
- `sin(θ) ≈ sin(θ_nom) + cos(θ_nom)·(θ − θ_nom)`
- `cos(θ) ≈ cos(θ_nom) − sin(θ_nom)·(θ − θ_nom)`
- Terapkan linearisasi ini pada **keduanya**:
  1. **Posisi vertikal effector `y_eff(δ)`** (agar invariant #3 `y_eff ≥ 0.15` tetap linier di Z3).
  2. **Torsi sendi elbow `τ₂(δ)`**.
- Set `θ_nom` = solusi IK numerik dari target (dihitung Python); Z3 hanya mencari deviasi `δ = θ − θ_nom` dalam `[−0.2, 0.2]` rad (plus `m_payload`) yang melanggar invarian. Model menjadi **`QF_LIA` murni**.

### Torsi (model linier quasi-statik)
`τ₂ ≈ (m_payload · g · L2_eff) · |cos(θ2_nom)| + m_link2 · g · L2_c · |cos(θ2_nom)|` — dengan `L2_eff` jarak horizontal efektif effector ke sendi elbow.

### Rumus bug (SAT)
IK buggy **tidak meng-clamp dekat singularitas maupun payload**: saat `‖target‖ → L1+L2+L3` (boundary workspace), ambil target `x = 0.70, y = 0.20` (`‖target‖ = 0.7280 m > 0.9 × 0.77 = 0.6930 m`) dengan `m_payload = 4.5 kg` → `τ₂ ≈ 4.5 · 9.81 · 0.35 ≈ 15.45 N·m > 8.0` → **`SAT`** (counterexample: elbow pada boundary). Assert test: `tau2 > 8.0` pada model buggy.

### Rumus fix (UNSAT)
Tambahkan di kontroler (bukan di `invariants_locked.py`!):
1. **Clamp workspace:** hanya terima target dengan `‖target‖ ≤ 0.9 · (L1 + L2 + L3) = 0.6930 m` dan `y_target ≥ 0.20 m`.
2. **Clamp payload & kecepatan deviasi:** `m_payload ≤ τ_max / (g · L2_eff · max(|cos(θ2_nom)|, 0.1))` dengan kompensasi deviasi `δ`.
Z3 fixed mengecek seluruh domain yang lolos kedua clamp → tak ada `δ` yang melanggar → **`UNSAT`**.

### Catatan `scene_adapter`
- Forward-kinematics 3 joint (Python) per tick → posisi segmen untuk Three.js primitives.
- Warna sendi merah bila `|τk| > 0.9 · τ_max` (peringatan) / `> τ_max` (pelanggaran, freeze-frame).

---

## Skenario C — `spatial_tiling` (Grid 3D Deadlock)

### Domain variabel

| Variabel | Range | Catatan |
|---|---|---|
| `workers` | `W = 4` konstanta | agen pekerja (`W1..W4`) |
| `grid` | `4×4×4` sel `(x, y, z ∈ [0, 3])` | sel di-encode sebagai ID integer `cell_id = x*16 + y*4 + z` |
| `tick` | `[0, 20]` | horizon 20 tick |
| `pos_w(t)`, `hold_w(t)` | sel integer (`Int`) | posisi & sel yang di-hold di Z3 |

### Kontrak invarian (locked)
1. **Mutual exclusion:** `∀ w ≠ w', ∀ t: hold_w(t) ≠ hold_w'(t)` (sel hold unik per tick).
2. **Deadlock-freedom:** tidak ada siklus tunggu *pairwise* (`w1` menunggu sel milik `w2` DAN `w2` menunggu sel milik `w1`) yang bertahan `≥ 4` tick berturut-turut.

### Encoding deadlock-freedom di Z3
- State tunggu: `waiting_on(w, w', t) = (pos_w(t) ≠ goal_w) ∧ (next_cell(w, t) == hold_w'(t))`.
- Semua variabel `Int` → `QF_LIA` murni, solve `< 0.5 s`.

### Rumus bug (SAT) — Terkalibrasi ke Tick 18
**Penting:** Jangan men-spawn `W1` & `W2` bersebelahan di tick 0 (jika bersebelahan di tick 0, deadlock langsung terjadi di tick 1–4, bukan tick 18).
* Gunakan spawn berjauhan yang berkonvergensi ke pusat grid pada **tick 14**:
  * `W1` mulai dari `(0, 0, 0)` menuju `(3, 3, 0)` melewati titik tengah `(1, 1, 0) → (2, 1, 0)`.
  * `W2` mulai dari `(3, 3, 0)` menuju `(0, 0, 0)` melewati titik tengah `(2, 1, 0) → (1, 1, 0)`.
  * Dengan kecepatan 1 sel per 3 tick (atau jalur memutar 14 langkah), `W1` memegang `(1, 1, 0)` dan meminta `(2, 1, 0)` pada **tick 14**, tepat saat `W2` memegang `(2, 1, 0)` dan meminta `(1, 1, 0)` **tanpa urutan kanonik**.
  * Siklus tunggu bertahan dari tick 14 → 15 → 16 → 17 → **tick 18** (`pairwise_wait_length = 4+` pada tick 18 → `DEADLOCK DETECTED at tick 18`).
* Assert test: `sat == True` dan `violated_tick == 18`.

### Rumus fix (UNSAT) — *canonical lock ordering*
Semua worker **wajib** mengunci pasangan `(sel_asal, sel_tujuan)` dalam urutan total global: `sort(key=(x, y, z))` / `min(cell_a, cell_b)` lebih dulu.
Implementasi di kontroler: sebelum masuk ke zona konflik, pekerja dengan ID sel target lebih kecil mendapat prioritas kunci penuh sehingga tidak pernah terjadi *hold-and-wait* silang. Z3 fixed membuktikan pada seluruh horizon 20 tick → **`UNSAT`**.

### Catatan `scene_adapter`
- Render kubus grid `4×4×4` 3D, panah ketergantungan merah antar worker yang saling tunggu.
- `violated_tick = 18` untuk freeze-frame demo.

---

## Ringkasan Kontrak Uji (untuk `verify.sh` / `pytest` Batch 1B)

| Skenario | `test_buggy` | `test_fixed` | Solver | Budget |
|---|---|---|---|---|
| `drone_swarm` | `SAT`, `min_dist < 0.5 m` @ tick 42 | `UNSAT` | `QF_NRA` kuadratik (tanpa sqrt) | `< 1 s` |
| `robot_arm` | `SAT`, `τ2 > 8.0` | `UNSAT` | `QF_LIA` (linearisasi Taylor) | `< 1 s` |
| `spatial_tiling` | `SAT`, deadlock @ tick 18 | `UNSAT` | `QF_LIA` (`Int`) | `< 0.5 s` |

**Aturan emas:** `invariants_locked.py` hanya berisi kontrak invarian (tabel di atas) — rumus bug & fix hidup di `buggy_impl.py` / kontroler, BUKAN di invariants. SHA-256 invariants dihitung sekali oleh `invariant_guard.py` sebelum run pertama.
