"""Scene exporter — maps scenario implementations into SceneTimelineFrame lists."""

from typing import Any

from scenarios.drone_swarm import scene_adapter as ds_scene
from scenarios.robot_arm import scene_adapter as ra_scene
from scenarios.spatial_tiling import scene_adapter as st_scene


def export_frames(
    scenario_id: str,
    fixed: bool = False,
    overrides: dict[str, float] | None = None,
) -> list[dict[str, Any]]:
    ov = overrides or {}
    if scenario_id == "drone_swarm":
        return ds_scene.build_timeline(fixed=fixed, r_safe_override=ov.get("r_safe_m"))
    if scenario_id == "robot_arm":
        return ra_scene.build_timeline(fixed=fixed, payload_override=ov.get("payload_kg"))
    if scenario_id == "spatial_tiling":
        return st_scene.build_timeline(fixed=fixed)
    raise ValueError(f"Unsupported scenario: {scenario_id}")
