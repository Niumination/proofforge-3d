"""Scene exporter — generates SceneTimelineFrame[] from scenario adapters."""

from scenarios.drone_swarm.scene_adapter import build_timeline as build_drone
from scenarios.robot_arm.scene_adapter import build_timeline as build_arm
from scenarios.spatial_tiling.scene_adapter import build_timeline as build_tiling


def export_frames(scenario_id: str, fixed: bool) -> list[dict]:
    if scenario_id == "drone_swarm":
        return build_drone(fixed=fixed)
    if scenario_id == "robot_arm":
        return build_arm(fixed=fixed)
    if scenario_id == "spatial_tiling":
        return build_tiling(fixed=fixed)
    raise ValueError(f"Unsupported scenario: {scenario_id}")
