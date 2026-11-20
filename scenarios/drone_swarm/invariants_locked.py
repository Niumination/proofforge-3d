"""Locked Z3 safety invariants for drone_swarm (IMMUTABLE)."""

from z3 import ArithRef, BoolRef

R_SAFE: float = 1.50
R_SAFE_SQ: float = R_SAFE * R_SAFE
INVARIANT_LABEL: str = "min_pairwise_distance >= 1.50m"


def z3_safety_condition(
    x_a: ArithRef,
    y_a: ArithRef,
    x_b: ArithRef,
    y_b: ArithRef,
) -> BoolRef:
    """Quadratic separation invariant without sqrt for exact Z3 solving."""
    dx = x_a - x_b
    dy = y_a - y_b
    return dx * dx + dy * dy >= R_SAFE_SQ
