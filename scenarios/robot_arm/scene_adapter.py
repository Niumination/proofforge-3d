"""Scene adapter for robot_arm — builds 41 frames of 3-DOF joint kinematics."""

import math

from scenarios.robot_arm.invariants_locked import L1, L2, L3, TAU_MAX, G

N_TICKS = 41
DT = 0.1


def build_timeline(fixed: bool, m_payload: float = 4.5) -> list[dict]:
    frames: list[dict] = []
    payload = min(m_payload, 1.7) if fixed else m_payload
    for k in range(N_TICKS):
        p = k / (N_TICKS - 1)
        if not fixed:
            t1 = 0.95 - 0.65 * p
            t2 = -0.05 - 0.25 * math.sin(p * math.pi)
            t3 = 0.15 * p
        else:
            t1 = 1.05 - 0.43 * p
            t2 = -0.35 - 0.20 * math.sin(p * math.pi)
            t3 = 0.08

        # Forward kinematics in XY plane (mapped to X, Y in 3D world)
        p0 = [0.0, 0.20, 0.0]
        p1 = [L1 * math.cos(t1), 0.20 + L1 * math.sin(t1), 0.0]
        p2 = [p1[0] + L2 * math.cos(t1 + t2), p1[1] + L2 * math.sin(t1 + t2), 0.0]
        p3 = [p2[0] + L3 * math.cos(t1 + t2 + t3), p2[1] + L3 * math.sin(t1 + t2 + t3), 0.0]

        # Torque ramps up near peak extension (tick 24..34)
        load_factor = 0.4 + 0.6 * math.sin(p * math.pi * 0.85)
        tau2 = payload * G * (L2 + L3) * abs(math.cos(t2)) * load_factor
        violated = (tau2 > TAU_MAX) or (p3[1] < 0.15)

        frames.append(
            {
                "tick": k,
                "time_sec": round(k * DT, 1),
                "is_violation": violated,
                "entities": [
                    {
                        "id": "arm-shoulder",
                        "kind": "arm_joint",
                        "position": [round(x, 3) for x in p0],
                        "rotation_euler": [0.0, 0.0, round(t1, 3)],
                        "velocity": [0.0, 0.0, 0.0],
                        "status": "OK",
                        "meta": {"next": [round(x, 3) for x in p1], "tau": round(tau2 * 0.7, 2)},
                    },
                    {
                        "id": "arm-elbow",
                        "kind": "arm_joint",
                        "position": [round(x, 3) for x in p1],
                        "rotation_euler": [0.0, 0.0, round(t1 + t2, 3)],
                        "velocity": [0.0, 0.0, 0.0],
                        "status": "TORQUE_BREACH" if violated else "OK",
                        "meta": {"next": [round(x, 3) for x in p2], "tau": round(tau2, 2)},
                    },
                    {
                        "id": "arm-effector",
                        "kind": "arm_effector",
                        "position": [round(x, 3) for x in p3],
                        "rotation_euler": [0.0, 0.0, round(t1 + t2 + t3, 3)],
                        "velocity": [0.0, 0.0, 0.0],
                        "status": "TORQUE_BREACH" if violated else "OK",
                        "meta": {"prev": [round(x, 3) for x in p2], "tau2": round(tau2, 2)},
                    },
                ],
                "constraints_overlay": [
                    {
                        "type": "torque_envelope",
                        "center": [round(x, 3) for x in p1],
                        "radius": 0.16,
                        "breached": violated,
                    }
                ],
            }
        )
    return frames
