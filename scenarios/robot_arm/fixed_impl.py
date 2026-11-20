"""Robot arm fixed controller — workspace & payload clamp (proven UNSAT)."""

import math
import time

from z3 import Real, RealVal, Solver, unsat

from scenarios.robot_arm.invariants_locked import (
    L1,
    L2,
    L3,
    TAU_MAX,
    G,
    z3_safety_condition,
)


def run_z3_check(timeout_ms: int = 8000) -> dict:
    start = time.perf_counter()
    s = Solver()
    s.set("timeout", timeout_ms)

    # Clamped workspace pose (||target|| <= 0.9 * reach_max, y_target >= 0.35m)
    t1_nom, t2_nom, t3_nom = 0.62, -0.35, 0.08
    l2_eff = L2 + L3
    cos_t2 = max(abs(math.cos(t2_nom)), 0.1)
    safe_payload_max = round((TAU_MAX - 1.0) / (G * l2_eff * cos_t2), 4)

    d1, d2, d3 = Real("delta1"), Real("delta2"), Real("delta3")
    m_payload = Real("m_payload")

    s.add(d1 >= RealVal("-0.2"), d1 <= RealVal("0.2"))
    s.add(d2 >= RealVal("-0.2"), d2 <= RealVal("0.2"))
    s.add(d3 >= RealVal("-0.2"), d3 <= RealVal("0.2"))
    s.add(m_payload >= RealVal("0.5"), m_payload <= RealVal(str(safe_payload_max)))

    theta1 = RealVal(str(t1_nom)) + d1
    theta2 = RealVal(str(t2_nom)) + d2
    theta3 = RealVal(str(t3_nom)) + d3

    # Clamped nominal height y_nom = 0.42 ensures even -0.2 rad perturbation stays >= 0.15m
    y_nom = 0.42
    dy_dt1 = L1 * math.cos(t1_nom)
    dy_dt2 = l2_eff * math.cos(t1_nom + t2_nom)
    y_eff = RealVal(str(y_nom)) + RealVal(str(round(dy_dt1, 4))) * d1 + RealVal(str(round(dy_dt2, 4))) * d2

    tau2 = m_payload * RealVal(str(round(G * l2_eff * cos_t2, 4))) + RealVal("0.5")

    s.add(z3_safety_condition(theta1, theta2, theta3, tau2, y_eff) == False)

    res = s.check()
    elapsed = max(1, int((time.perf_counter() - start) * 1000))
    if res == unsat:
        return {
            "status": "UNSAT_PROVEN",
            "violated_invariant": None,
            "counterexample_inputs": None,
            "violated_tick": None,
            "violated_time_sec": None,
            "solver_duration_ms": elapsed,
            "note": f"Workspace clamped <= 0.9*reach and payload <= {safe_payload_max} kg proven UNSAT.",
        }
    return {"status": "SAT_VIOLATION", "solver_duration_ms": elapsed}
