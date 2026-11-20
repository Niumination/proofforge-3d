"""Locked Z3 safety invariants for spatial_tiling (IMMUTABLE)."""

from z3 import And, BoolRef, Not

GRID_SIZE: int = 4
MAX_TICKS: int = 20
DEADLOCK_THRESHOLD: int = 4
INVARIANT_LABEL: str = "mutual_exclusion & deadlock_freedom (< 4 ticks)"


def cell_id(x: int, y: int, z: int) -> int:
    return x * 16 + y * 4 + z


def z3_no_pairwise_deadlock(
    hold_1: list,
    req_1: list,
    hold_2: list,
    req_2: list,
) -> BoolRef:
    """Forbid pairwise circular wait lasting >= 4 consecutive ticks."""
    no_deadlock_clauses = []
    for t in range(len(hold_1) - DEADLOCK_THRESHOLD + 1):
        window = []
        for dt in range(DEADLOCK_THRESHOLD):
            k = t + dt
            pair_wait = And(
                hold_1[k] == req_2[k],
                hold_2[k] == req_1[k],
                hold_1[k] != hold_2[k],
            )
            window.append(pair_wait)
        no_deadlock_clauses.append(Not(And(*window)))
    return And(*no_deadlock_clauses)
