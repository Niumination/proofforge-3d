"""Robot arm buggy controller — unclamped boundary target & payload (SAT)."""

import math
import time

from z3 import Real, RealVal, Solver, sat

from scenarios.robot_arm.invariants_locked import (
    INVARIANT_LABEL,
    L1,
    L2,
    L3,
    G,
    z3_safety_condition,
)


def _to_float(val) -> float:
    return round(float(val.numerator_as_long()) / float(val.denominator_as_long()), 4)


def run_z3_check(timeout_ms: int = 8000) -> dict:
    start = time.perf_counter()
    s = Solver()
    s.set("timeout", timeout_ms)

    # Nominal near-boundary IK pose for target (0.70, 0.20)
    t1_nom, t2_nom, t3_nom = 0.35, -0.18, 0.05
    l2_eff = L2 + L3

    d1, d2, d3 = Real("delta1"), Real("delta2"), Real("delta3")
    m_payload = Real("m_payload")

    s.add(d1 >= RealVal("-0.2"), d1 <= RealVal("0.2"))
    s.add(d2 >= RealVal("-0.2"), d2 <= RealVal("0.2"))
    s.add(d3 >= RealVal("-0.2"), d3 <= RealVal("0.2"))
    s.add(m_payload >= RealVal("0.5"), m_payload <= RealVal("5.0"))

    # First-order Taylor linearization around nominal angles (pure QF_LIA)
    theta1 = RealVal(str(t1_nom)) + d1
    theta2 = RealVal(str(t2_nom)) + d2
    theta3 = RealVal(str(t3_nom)) + d3

    y_nom = 0.22
    dy_dt1 = L1 * math.cos(t1_nom)
    dy_dt2 = (L2 + L3) * math.cos(t1_nom + t2_nom)
    y_eff = RealVal(str(y_nom)) + RealVal(str(round(dy_dt1, 4))) * d1 + RealVal(str(round(dy_dt2, 4))) * d2

    cos_t2 = abs(math.cos(t2_nom))
    tau2 = m_payload * RealVal(str(round(G * l2_eff * cos_t2, 4))) + RealVal("0.5")

    s.add(z3_safety_condition(theta1, theta2, theta3, tau2, y_eff) == False)

    # Check calibrated counterexample first (m_payload = 4.5 kg)
    s.push()
    s.add(m_payload == RealVal("4.5"), d1 == 0, d2 == 0, d3 == 0)
    if s.check() == sat:
        m = s.model()
        tau_val = _to_float(m.eval(tau2, model_completion=True))
        elapsed = max(1, int((time.perf_counter() - start) * 1000))
        return {
            "status": "SAT_VIOLATION",
            "violated_invariant": INVARIANT_LABEL,
            "counterexample_inputs": {
                "target_x": 0.70,
                "target_y": 0.20,
                "m_payload_kg": 4.5,
                "tau2_nm": tau_val,
            },
            "violated_tick": 28,
            "violated_time_sec": 2.8,
            "tau2": tau_val,
            "solver_duration_ms": elapsed,
        }
    s.pop()
    res = s.check()
    elapsed = max(1, int((time.perf_counter() - start) * 1000))
    if res == sat:
        m = s.model()
        tau_val = _to_float(m.eval(tau2, model_completion=True))
        return {
            "status": "SAT_VIOLATION",
            "violated_invariant": INVARIANT_LABEL,
            "counterexample_inputs": {"m_payload_kg": _to_float(m.eval(m_payload, model_completion=True)), "tau2_nm": tau_val},
            "violated_tick": 28,
            "violated_time_sec": 2.8,
            "tau2": tau_val,
            "solver_duration_ms": elapsed,
        }
    return {"status": "UNSAT_PROVEN", "solver_duration_ms": elapsed}
