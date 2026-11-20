import asyncio
import json
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from apps.api.agents.deterministic_sim import DeterministicSim
from apps.api.models.schemas import ForgeRunRequest

router = APIRouter()

_runs: dict[str, dict] = {}
SUPPORTED_SCENARIOS = {"drone_swarm", "robot_arm", "spatial_tiling"}


@router.post("/api/forge/run")
async def forge_run(request: ForgeRunRequest) -> dict:
    if request.scenario_id not in SUPPORTED_SCENARIOS:
        raise HTTPException(status_code=400, detail=f"Unsupported scenario: {request.scenario_id}")

    sim = DeterministicSim()
    pipeline_out = sim.run_pipeline(
        scenario_id=request.scenario_id,
        inject_initial_bug=request.inject_initial_bug,
        enable_adversarial_hook_test=request.enable_adversarial_hook_test,
    )
    run_id = f"run-{request.scenario_id}-{uuid.uuid4().hex[:8]}"
    _runs[run_id] = {"request": request.model_dump(), "pipeline": pipeline_out}
    return {"runId": run_id}


def _sse_pack(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


@router.get("/api/forge/stream/{run_id}")
async def forge_stream(run_id: str) -> StreamingResponse:
    store = _runs.get(run_id)
    if not store:
        raise HTTPException(status_code=404, detail="run not found")

    pipeline = store["pipeline"]

    async def event_gen():
        yield _sse_pack(
            "STAGE_CHANGED",
            {"stage": "LOCK_INVARIANTS", "invariant_sha256": pipeline["invariant_sha256"]},
        )
        await asyncio.sleep(0.02)

        for hook_ev in pipeline["hook_events"]:
            yield _sse_pack("HOOK_AUDIT", hook_ev)
            await asyncio.sleep(0.02)

        yield _sse_pack("STAGE_CHANGED", {"stage": "VERIFY"})
        iterations = pipeline["iterations"]

        if len(iterations) == 2:
            it1 = iterations[0]
            yield _sse_pack(
                "VERIFICATION_RESULT",
                {"phase": "before", "result": it1["result"], "frames": it1["frames"]},
            )
            await asyncio.sleep(0.05)

            yield _sse_pack("STAGE_CHANGED", {"stage": "PATCH"})
            yield _sse_pack(
                "PATCH_DIFF",
                {
                    "scenario_id": pipeline["scenario_id"],
                    "diff": pipeline["patch_diff"],
                },
            )
            await asyncio.sleep(0.05)

            it2 = iterations[1]
            yield _sse_pack(
                "VERIFICATION_RESULT",
                {"phase": "after", "result": it2["result"], "frames": it2["frames"]},
            )
        else:
            it = iterations[0]
            yield _sse_pack(
                "VERIFICATION_RESULT",
                {"phase": "after", "result": it["result"], "frames": it["frames"]},
            )

        yield _sse_pack("STAGE_CHANGED", {"stage": "COMPLETE"})

    return StreamingResponse(event_gen(), media_type="text/event-stream")
