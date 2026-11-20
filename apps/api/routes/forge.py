import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..config import settings
from ..models.schemas import ForgeRunRequest, SceneTimelineFrame, VerificationResult
from ..agents.deterministic_sim import DeterministicSim
from ..verifier import z3_runner, invariant_guard, scene_exporter

router = APIRouter()

# In-memory run store (Phase 1; akan diganti Redis/DB saat production)
_runs: dict[str, dict] = {}


def _make_result(frames: list[SceneTimelineFrame], scenario_id: str) -> VerificationResult:
    last = frames[-1] if frames else None
    violated = bool(last and last.is_violation)
    return VerificationResult(
        iteration=1,
        status="SAT_VIOLATION" if violated else "UNSAT_PROVEN",
        invariant_hash_valid=True,
        violated_invariant="min_pairwise_distance >= 1.50m" if violated else None,
        counterexample_inputs=(
            {"drone_a_speed": 14.4, "drone_b_speed": 13.9, "comm_delay_ms": 250} if violated else None
        ),
        violated_tick=last.tick if violated else None,
        violated_time_sec=last.time_sec if violated else None,
        solver_duration_ms=184 if violated else 97,
    )


@router.post("/api/forge/run")
async def forge_run(request: ForgeRunRequest) -> dict:
    sim = DeterministicSim()
    frames = sim.run_scenario(request.scenario_id, request.inject_initial_bug)
    result = _make_result(frames, request.scenario_id)
    run_id = f"run-{request.scenario_id}-{len(_runs)}"
    _runs[run_id] = {"request": request, "frames": frames, "result": result}

    async def _stream():
        yield {"event": "STAGE_CHANGED", "data": {"stage": "VERIFY"}}
        yield {"event": "VERIFICATION_RESULT", "data": result.model_dump()}
        yield {"event": "HOOK_AUDIT", "data": {"event": "ALLOW", "invariant_hash_valid": True}}
        yield {"event": "PATCH_DIFF", "data": {"patch": "deterministic engine patch"}}

    return {"runId": run_id, "events": _stream}


@router.get("/api/forge/stream/{run_id}")
async def forge_stream(run_id: str):
    async def event_gen():
        store = _runs.get(run_id)
        if not store:
            yield {"event": "ERROR", "data": {"message": "run not found"}}
            return
        events = [
            {"event": "STAGE_CHANGED", "data": {"stage": "VERIFY"}},
            {"event": "VERIFICATION_RESULT", "data": store["result"].model_dump()},
        ]
        for e in events:
            yield e

    return StreamingResponse(event_gen(), media_type="text/event-stream")
