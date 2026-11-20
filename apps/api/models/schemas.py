from pydantic import BaseModel, Field


class ForgeRunRequest(BaseModel):
    scenario_id: str = Field(..., description="drone_swarm | robot_arm | spatial_tiling")
    mode: str = Field(default="deterministic")
    custom_spec: str | None = None
    inject_initial_bug: bool = False
    max_iterations: int = 5
    enable_adversarial_hook_test: bool = False


class VerificationResult(BaseModel):
    iteration: int
    status: str
    invariant_hash_valid: bool
    violated_invariant: str | None = None
    counterexample_inputs: dict[str, float] | None = None
    violated_tick: int | None = None
    violated_time_sec: float | None = None
    solver_duration_ms: int = 0


class SceneEntity(BaseModel):
    id: str
    kind: str
    position: list[float]
    rotation_euler: list[float]
    velocity: list[float]
    status: str


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
    data: dict = {}
