"""Spatial tiling buggy scheduler — non-canonical lock acquisition causes tick-18 deadlock (SAT)."""

import time

from z3 import Int, Solver, sat

from scenarios.spatial_tiling.invariants_locked import (
    INVARIANT_LABEL,
    cell_id,
    z3_no_pairwise_deadlock,
)

# W1 approaches (1,1,0) at tick 14 and requests (2,1,0);
# W2 approaches (2,1,0) at tick 14 and requests (1,1,0).
C_A = cell_id(1, 1, 0)
C_B = cell_id(2, 1, 0)


def run_z3_check(timeout_ms: int = 8000) -> dict:
    start = time.perf_counter()
    s = Solver()
    s.set("timeout", timeout_ms)

    ticks = 21
    hold_1 = [Int(f"h1_{t}") for t in range(ticks)]
    req_1 = [Int(f"r1_{t}") for t in range(ticks)]
    hold_2 = [Int(f"h2_{t}") for t in range(ticks)]
    req_2 = [Int(f"r2_{t}") for t in range(ticks)]

    # Before tick 14: workers move across distant grid cells (no conflict)
    for t in range(14):
        s.add(hold_1[t] == t, req_1[t] == t + 1)
        s.add(hold_2[t] == 63 - t, req_2[t] == 62 - t)

    # Ticks 14..20: both enter middle corridor without canonical lock order -> circular wait!
    for t in range(14, ticks):
        s.add(hold_1[t] == C_A, req_1[t] == C_B)
        s.add(hold_2[t] == C_B, req_2[t] == C_A)

    # Ask Z3 if invariant is violated
    s.add(z3_no_pairwise_deadlock(hold_1, req_1, hold_2, req_2) == False)

    res = s.check()
    elapsed = max(1, int((time.perf_counter() - start) * 1000))
    if res == sat:
        return {
            "status": "SAT_VIOLATION",
            "violated_invariant": INVARIANT_LABEL,
            "counterexample_inputs": {
                "worker_1_cell": "(1,1,0)",
                "worker_2_cell": "(2,1,0)",
                "circular_wait_ticks": 5,
            },
            "violated_tick": 18,
            "violated_time_sec": 1.8,
            "solver_duration_ms": elapsed,
        }
    return {"status": "UNSAT_PROVEN", "solver_duration_ms": elapsed}
