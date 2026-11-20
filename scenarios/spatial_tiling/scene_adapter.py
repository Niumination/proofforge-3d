"""Scene adapter for spatial_tiling — 4 workers on 4x4x4 grid across 21 ticks."""

N_TICKS = 21
DT = 0.1


def _lerp_cell(a: tuple[int, int, int], b: tuple[int, int, int], frac: float) -> list[float]:
    return [
        round(a[0] + (b[0] - a[0]) * frac, 2),
        round(a[1] + (b[1] - a[1]) * frac, 2),
        round(a[2] + (b[2] - a[2]) * frac, 2),
    ]


def build_timeline(fixed: bool) -> list[dict]:
    frames: list[dict] = []
    for k in range(N_TICKS):
        if k <= 14:
            frac = k / 14.0
            w1 = _lerp_cell((0, 0, 0), (1, 1, 0), frac)
            w2 = _lerp_cell((3, 3, 0), (2, 1, 0), frac)
            violated = False
        elif not fixed:
            w1 = [1.0, 1.0, 0.0]
            w2 = [2.0, 1.0, 0.0]
            violated = k >= 17
        else:
            frac = (k - 14) / 6.0
            w1 = _lerp_cell((1, 1, 0), (3, 3, 0), frac)
            w2 = _lerp_cell((2, 2, 0), (0, 0, 0), frac)
            violated = False

        w3 = _lerp_cell((0, 3, 2), (3, 0, 2), k / (N_TICKS - 1))
        w4 = _lerp_cell((3, 0, 3), (0, 3, 3), k / (N_TICKS - 1))

        frames.append(
            {
                "tick": k,
                "time_sec": round(k * DT, 1),
                "is_violation": violated,
                "entities": [
                    {
                        "id": "worker-1",
                        "kind": "grid_worker",
                        "position": w1,
                        "rotation_euler": [0.0, 0.0, 0.0],
                        "velocity": [0.0, 0.0, 0.0],
                        "status": "DEADLOCK" if violated else "OK",
                    },
                    {
                        "id": "worker-2",
                        "kind": "grid_worker",
                        "position": w2,
                        "rotation_euler": [0.0, 0.0, 0.0],
                        "velocity": [0.0, 0.0, 0.0],
                        "status": "DEADLOCK" if violated else "OK",
                    },
                    {
                        "id": "worker-3",
                        "kind": "grid_worker",
                        "position": w3,
                        "rotation_euler": [0.0, 0.0, 0.0],
                        "velocity": [0.0, 0.0, 0.0],
                        "status": "OK",
                    },
                    {
                        "id": "worker-4",
                        "kind": "grid_worker",
                        "position": w4,
                        "rotation_euler": [0.0, 0.0, 0.0],
                        "velocity": [0.0, 0.0, 0.0],
                        "status": "OK",
                    },
                ],
                "constraints_overlay": [
                    {
                        "type": "deadlock_link",
                        "center": [1.5, 1.0, 0.0],
                        "radius": 0.9,
                        "breached": violated,
                    }
                ],
            }
        )
    return frames
