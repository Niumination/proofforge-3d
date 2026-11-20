"""Z3 runner — executes real Z3 SMT verification for scenarios."""

from typing import Any

from scenarios.drone_swarm import buggy_impl as ds_buggy
from scenarios.drone_swarm import fixed_impl as ds_fixed
from scenarios.robot_arm import buggy_impl as ra_buggy
from scenarios.robot_arm import fixed_impl as ra_fixed
from scenarios.spatial_tiling import buggy_impl as st_buggy
from scenarios.spatial_tiling import fixed_impl as st_fixed


def run_z3(scenario_id: str, fixed: bool = False, timeout_ms: int = 8000) -> dict[str, Any]:
    dispatch = {
        "drone_swarm": (ds_buggy, ds_fixed),
        "robot_arm": (ra_buggy, ra_fixed),
        "spatial_tiling": (st_buggy, st_fixed),
    }
    pair = dispatch.get(scenario_id)
    if not pair:
        return {"status": "ERROR", "solver_duration_ms": 0, "note": f"Unknown scenario: {scenario_id}"}
    module = pair[1] if fixed else pair[0]
    return module.run_z3_check(timeout_ms=timeout_ms)
