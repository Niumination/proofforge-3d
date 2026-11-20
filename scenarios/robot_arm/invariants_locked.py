"""Locked Z3 safety invariants for robot_arm (IMMUTABLE)."""

from z3 import And, ArithRef, BoolRef, RealVal

L1: float = 0.35
L2: float = 0.30
L3: float = 0.12
REACH_MAX: float = L1 + L2 + L3  # 0.77 m
TAU_MAX: float = 8.0
Y_EFF_MIN: float = 0.15
G: float = 9.81

THETA1_MIN, THETA1_MAX = -1.5708, 1.5708
THETA2_MIN, THETA2_MAX = -2.0944, 2.0944
THETA3_MIN, THETA3_MAX = -1.5708, 1.5708

INVARIANT_LABEL: str = "|tau2| <= 8.0 N·m & y_eff >= 0.15m"


def z3_safety_condition(
    theta1: ArithRef,
    theta2: ArithRef,
    theta3: ArithRef,
    tau2: ArithRef,
    y_eff: ArithRef,
) -> BoolRef:
    return And(
        theta1 >= RealVal(str(THETA1_MIN)),
        theta1 <= RealVal(str(THETA1_MAX)),
        theta2 >= RealVal(str(THETA2_MIN)),
        theta2 <= RealVal(str(THETA2_MAX)),
        theta3 >= RealVal(str(THETA3_MIN)),
        theta3 <= RealVal(str(THETA3_MAX)),
        tau2 >= RealVal(str(-TAU_MAX)),
        tau2 <= RealVal(str(TAU_MAX)),
        y_eff >= RealVal(str(Y_EFF_MIN)),
    )
