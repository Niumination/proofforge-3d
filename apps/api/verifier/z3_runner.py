"""Z3 runner — executes real Z3 SMT verification with optional live constraint overrides."""

import re
from typing import Any

from scenarios.drone_swarm import buggy_impl as ds_buggy
from scenarios.drone_swarm import fixed_impl as ds_fixed
from scenarios.robot_arm import buggy_impl as ra_buggy
from scenarios.robot_arm import fixed_impl as ra_fixed
from scenarios.spatial_tiling import buggy_impl as st_buggy
from scenarios.spatial_tiling import fixed_impl as st_fixed


def parse_constraint_overrides(custom_spec: str | None) -> dict[str, float]:
    if not custom_spec:
        return {}
    overrides: dict[str, float] = {}
    for key in ("r_safe_m", "payload_kg", "tau_max_nm", "comm_delay_ms", "max_wait_ticks"):
        m = re.search(rf"{key}\s*=\s*(\d+(?:\.\d+)?)", custom_spec)
        if m:
            overrides[key] = float(m.group(1))
    return overrides


def run_z3(
    scenario_id: str,
    fixed: bool = False,
    timeout_ms: int = 8000,
    overrides: dict[str, float] | None = None,
) -> dict[str, Any]:
    ov = overrides or {}
    if scenario_id == "drone_swarm":
        mod = ds_fixed if fixed else ds_buggy
        return mod.run_z3_check(timeout_ms=timeout_ms, r_safe_override=ov.get("r_safe_m"))
    if scenario_id == "robot_arm":
        mod = ra_fixed if fixed else ra_buggy
        return mod.run_z3_check(timeout_ms=timeout_ms, payload_override=ov.get("payload_kg"))
    if scenario_id == "spatial_tiling":
        mod = st_fixed if fixed else st_buggy
        return mod.run_z3_check(timeout_ms=timeout_ms)
    return {"status": "ERROR", "solver_duration_ms": 0, "note": f"Unknown scenario: {scenario_id}"}
