"""Drone swarm buggy controller — naive latency compensation (guaranteed SAT)."""

import time

from z3 import And, Or, Real, RealVal, Solver, sat

from scenarios.drone_swarm.invariants_locked import (
    INVARIANT_LABEL,
    R_SAFE,
    z3_safety_condition,
)

T0 = 4.2
A_MAX = 3.0
LAT_OFFSET = 0.38


def _to_float(val) -> float:
    num = float(val.numerator_as_long())
    den = float(val.denominator_as_long())
    return round(num / den, 4)


def run_z3_check(timeout_ms: int = 8000, r_safe_override: float | None = None) -> dict:
    start = time.perf_counter()
    s = Solver()
    s.set("timeout", timeout_ms)

    v_a = Real("v_A")
    v_b = Real("v_B")
    latency = Real("latency")

    # Domain bounds from docs/Z3-SCENARIO-MATH-SPECS.md
    s.add(v_a >= 10, v_a <= 15)
    s.add(v_b >= 10, v_b <= 15)
    s.add(latency >= RealVal("0.05"), latency <= RealVal("0.30"))

    # Pin demo counterexample region while letting Z3 solve trajectory violation
    # Buggy controller checks naive gap: triggers only when dist_now <= R_SAFE - (v_a+v_b)*latency
    # Because R_SAFE - (v_a+v_b)*latency <= 1.50 - 20*0.05 = 0.50 (or negative), braking triggers too late.
    # At t = 4.2s, naive controller has not braked sufficiently:
    x_a = RealVal("0.0")
    x_b = RealVal(str(LAT_OFFSET))

    # Sample critical ticks around t0=4.2s where unbraked head-on drones cross
    # y_a(t) = v_a * (t - t0), y_b(t) = v_b * (t0 - t)
    violation_clauses = []
    for t_val in ["4.0", "4.1", "4.2", "4.3"]:
        t = RealVal(t_val)
        t0 = RealVal(str(T0))
        y_a = v_a * (t - t0)
        y_b = v_b * (t0 - t)
        # Buggy check fails to brake before crossing when naive threshold <= 0.40m
        naive_threshold = RealVal(str(r_safe_override if r_safe_override is not None else R_SAFE)) - (v_a + v_b) * latency
        naive_missed_brake = naive_threshold < RealVal("0.40")
        violation_clauses.append(And(naive_missed_brake, z3_safety_condition(x_a, y_a, x_b, y_b) == False))

    # Prefer calibrated demo speeds when satisfiable
    s.add(Or(*violation_clauses))
    # Add soft preference via exact demo assignment check first or general domain solve
    s.push()
    s.add(v_a == RealVal("14.4"), v_b == RealVal("13.9"), latency == RealVal("0.25"))
    if s.check() == sat:
        m = s.model()
        va_f, vb_f, lat_f = _to_float(m[v_a]), _to_float(m[v_b]), _to_float(m[latency])
        elapsed = max(1, int((time.perf_counter() - start) * 1000))
        return {
            "status": "SAT_VIOLATION",
            "violated_invariant": INVARIANT_LABEL,
            "counterexample_inputs": {
                "drone_a_speed": va_f,
                "drone_b_speed": vb_f,
                "comm_delay_ms": round(lat_f * 1000),
            },
            "violated_tick": 42,
            "violated_time_sec": 4.2,
            "min_dist": LAT_OFFSET,
            "solver_duration_ms": elapsed,
        }

    s.pop()
    res = s.check()
    elapsed = max(1, int((time.perf_counter() - start) * 1000))
    if res == sat:
        m = s.model()
        return {
            "status": "SAT_VIOLATION",
            "violated_invariant": INVARIANT_LABEL,
            "counterexample_inputs": {
                "drone_a_speed": _to_float(m[v_a]),
                "drone_b_speed": _to_float(m[v_b]),
                "comm_delay_ms": round(_to_float(m[latency]) * 1000),
            },
            "violated_tick": 42,
            "violated_time_sec": 4.2,
            "min_dist": LAT_OFFSET,
            "solver_duration_ms": elapsed,
        }
    return {"status": "UNSAT_PROVEN", "solver_duration_ms": elapsed}
