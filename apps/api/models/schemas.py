from typing import Any

from pydantic import BaseModel, Field


class ForgeRunRequest(BaseModel):
    scenario_id: str = Field(..., description="drone_swarm | robot_arm | spatial_tiling")
    mode: str = Field(default="deterministic")
    custom_spec: str | None = None
    inject_initial_bug: bool = True
    max_iterations: int = 5
    enable_adversarial_hook_test: bool = False


class VerificationResult(BaseModel):
    iteration: int
    status: str
    invariant_hash_valid: bool
    invariant_sha256: str = ""
    violated_invariant: str | None = None
    counterexample_inputs: dict[str, Any] | None = None
    violated_tick: int | None = None
    violated_time_sec: float | None = None
    solver_duration_ms: int = 0
    note: str | None = None


class SceneEntity(BaseModel):
    id: str
    kind: str
    position: list[float]
    rotation_euler: list[float]
    velocity: list[float]
    status: str
    meta: dict[str, Any] | None = None


class ConstraintsOverlay(BaseModel):
    type: str
    center: list[float]
    radius: float
    breached: bool


class SceneTimelineFrame(BaseModel):
    tick: int
    time_sec: float
    is_violation: bool
    entities: list[SceneEntity]
    constraints_overlay: list[ConstraintsOverlay]


class SSEStreamEvent(BaseModel):
    type: str
    data: dict[str, Any] = Field(default_factory=dict)


class ProofExportRequest(BaseModel):
    scenario_id: str
    result: VerificationResult


class ProofExportResponse(BaseModel):
    export_url: str
    proxy_audit: dict[str, Any]
