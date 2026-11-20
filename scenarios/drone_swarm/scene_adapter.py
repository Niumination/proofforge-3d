"""Scene adapter for drone_swarm — builds 101 SceneTimelineFrame objects."""

import math

from scenarios.drone_swarm.invariants_locked import R_SAFE

DT = 0.1
N_TICKS = 101
T0 = 4.2
A_MAX = 3.0
LAT_OFFSET = 0.38


def build_timeline(
    fixed: bool,
    v_a: float = 14.4,
    v_b: float = 13.9,
    latency: float = 0.25,
) -> list[dict]:
    required_gap = R_SAFE + (v_a + v_b) * latency + (v_a**2 + v_b**2) / (2.0 * A_MAX)
    init_gap = (v_a + v_b) * T0
    trig_time = max(0.0, (init_gap - required_gap) / (v_a + v_b))

    v_a_t: list[float] = []
    v_b_t: list[float] = []
    for k in range(N_TICKS):
        t = k * DT
        if not fixed:
            v_a_t.append(v_a)
            v_b_t.append(v_b)
        else:
            brake_elapsed = max(0.0, t - (trig_time + latency))
            v_a_t.append(max(0.0, v_a - A_MAX * brake_elapsed))
            v_b_t.append(max(0.0, v_b - A_MAX * brake_elapsed))

    frames: list[dict] = []
    s_a = 0.0
    s_b = 0.0
    for k in range(N_TICKS):
        t = round(k * DT, 2)
        if k > 0:
            s_a += v_a_t[k] * DT
            s_b += v_b_t[k] * DT
        z_a = -v_a * T0 + s_a
        z_b = v_b * T0 - s_b
        dist = math.hypot(LAT_OFFSET - 0.0, z_b - z_a)
        violated = dist < R_SAFE
        frames.append(
            {
                "tick": k,
                "time_sec": round(t, 1),
                "is_violation": violated,
                "entities": [
                    {
                        "id": "drone-alpha",
                        "kind": "quadrotor",
                        "position": [0.0, 0.8, round(z_a, 3)],
                        "rotation_euler": [0.0, 0.0, 0.0],
                        "velocity": [0.0, 0.0, round(v_a_t[k], 3)],
                        "status": "COLLISION" if violated else "OK",
                    },
                    {
                        "id": "drone-beta",
                        "kind": "quadrotor",
                        "position": [LAT_OFFSET, 0.8, round(z_b, 3)],
                        "rotation_euler": [0.0, math.pi, 0.0],
                        "velocity": [0.0, 0.0, round(-v_b_t[k], 3)],
                        "status": "COLLISION" if violated else "OK",
                    },
                ],
                "constraints_overlay": [
                    {
                        "type": "safety_sphere",
                        "center": [0.0, 0.8, round(z_a, 3)],
                        "radius": R_SAFE,
                        "breached": violated,
                    },
                    {
                        "type": "safety_sphere",
                        "center": [LAT_OFFSET, 0.8, round(z_b, 3)],
                        "radius": R_SAFE,
                        "breached": violated,
                    },
                ],
            }
        )
    return frames
