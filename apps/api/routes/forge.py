import asyncio
import json
import re
import uuid

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from apps.api.agents.argon_synth import parse_voice_constraint_gemini
from apps.api.agents.closed_loop import ClosedLoopOrchestrator
from apps.api.config import settings
from apps.api.models.schemas import (
    ForgeRunRequest,
    RedTeamRequest,
    VoiceConstraintRequest,
    VoiceConstraintResponse,
)
from apps.api.security.protected_hooks import (
    detect_prompt_injection,
    evaluate_invariant_patch_attempt,
    evaluate_write_scope,
)
from apps.api.verifier.invariant_guard import compute_invariant_hash

router = APIRouter()

_runs: dict[str, dict] = {}
SUPPORTED_SCENARIOS = {"drone_swarm", "robot_arm", "spatial_tiling"}


@router.post("/api/forge/run")
async def forge_run(request: ForgeRunRequest) -> dict:
    if request.scenario_id not in SUPPORTED_SCENARIOS:
        raise HTTPException(status_code=400, detail=f"Unsupported scenario: {request.scenario_id}")

    orch = ClosedLoopOrchestrator()
    pipeline_out = orch.run(
        scenario_id=request.scenario_id,
        mode=request.mode,
        custom_spec=request.custom_spec,
        inject_initial_bug=request.inject_initial_bug,
        max_iterations=request.max_iterations,
        enable_adversarial_hook_test=request.enable_adversarial_hook_test,
        simulate_prompt_injection=request.simulate_prompt_injection,
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
        await asyncio.sleep(0.01)

        for log_ev in pipeline.get("agent_logs", []):
            yield _sse_pack("AGENT_LOG", log_ev)
            await asyncio.sleep(0.01)

        for hook_ev in pipeline["hook_events"]:
            yield _sse_pack("HOOK_AUDIT", hook_ev)
            await asyncio.sleep(0.01)

        yield _sse_pack("STAGE_CHANGED", {"stage": "VERIFY"})
        iterations = pipeline["iterations"]

        if len(iterations) >= 2:
            it1 = iterations[0]
            yield _sse_pack(
                "VERIFICATION_RESULT",
                {"phase": "before", "result": it1["result"], "frames": it1["frames"]},
            )
            await asyncio.sleep(0.03)

            yield _sse_pack("STAGE_CHANGED", {"stage": "PATCH"})
            yield _sse_pack(
                "PATCH_DIFF",
                {
                    "scenario_id": pipeline["scenario_id"],
                    "diff": pipeline["patch_diff"],
                },
            )
            await asyncio.sleep(0.03)

            it_last = iterations[-1]
            yield _sse_pack(
                "VERIFICATION_RESULT",
                {"phase": "after", "result": it_last["result"], "frames": it_last["frames"]},
            )
        else:
            it = iterations[0]
            yield _sse_pack(
                "VERIFICATION_RESULT",
                {"phase": "after", "result": it["result"], "frames": it["frames"]},
            )

        if pipeline.get("certificate"):
            yield _sse_pack("PROOF_CERTIFICATE", pipeline["certificate"])

        yield _sse_pack("STAGE_CHANGED", {"stage": "COMPLETE"})

    return StreamingResponse(event_gen(), media_type="text/event-stream")


@router.post("/api/forge/redteam")
async def forge_redteam(req: RedTeamRequest) -> dict:
    """Execute 3-vector adversarial attack test against Protected Hooks (PF-025)."""
    base_sha = compute_invariant_hash("R_SAFE = 1.50\n")
    events = [
        evaluate_invariant_patch_attempt(base_sha, "R_SAFE = 0.01\n"),
        evaluate_write_scope("scenarios/drone_swarm/invariants_locked.py"),
        *detect_prompt_injection(req.attack_prompt),
    ]
    blocked = [ev for ev in events if ev.get("action") == "BLOCKED"]
    return {
        "scenario_id": req.scenario_id,
        "all_blocked": len(blocked) == len(events) and len(blocked) >= 3,
        "blocked_count": len(blocked),
        "hook_events": events,
    }


@router.post("/api/forge/voice-constraint", response_model=VoiceConstraintResponse)
async def forge_voice_constraint(req: VoiceConstraintRequest) -> VoiceConstraintResponse:
    """Parse voice/natural-language constraint adjustments (PF-026)."""
    if settings.proofforge_mode == "live_gemini" and settings.gemini_api_key:
        try:
            parsed = parse_voice_constraint_gemini(req.transcript, req.scenario_id)
            sc = str(parsed.get("scenario_id", req.scenario_id))
            if sc not in SUPPORTED_SCENARIOS:
                sc = req.scenario_id
            param = str(parsed.get("parameter", "r_safe_m"))
            val = float(parsed.get("value", 2.0))
            unit = str(parsed.get("unit", "m"))
            return VoiceConstraintResponse(
                scenario_id=sc,
                parameter=param,
                value=val,
                unit=unit,
                summary=str(parsed.get("summary", f"{sc}.{param} = {val} {unit}")),
                custom_spec_patch=f"Enforce {param}={val}{unit} on scenario {sc}",
                source=settings.gemini_fast_model,
            )
        except (httpx.HTTPError, RuntimeError, ValueError):
            pass

    text = req.transcript.strip()
    lower = text.lower()

    target_scenario = req.scenario_id
    if "robot" in lower or "arm" in lower or "torque" in lower or "payload" in lower:
        target_scenario = "robot_arm"
    elif "tile" in lower or "grid" in lower or "deadlock" in lower:
        target_scenario = "spatial_tiling"
    elif "drone" in lower or "swarm" in lower or "separation" in lower:
        target_scenario = "drone_swarm"

    num_match = re.search(r"(\d+(?:\.\d+)?)", lower)
    num_val = float(num_match.group(1)) if num_match else 2.0

    if target_scenario == "robot_arm":
        param, unit = (
            ("payload_kg", "kg") if "payload" in lower else ("tau_max_nm", "N·m")
        )
    elif target_scenario == "spatial_tiling":
        param, unit = "max_wait_ticks", "ticks"
    else:
        param, unit = (
            ("comm_delay_ms", "ms")
            if ("latency" in lower or "delay" in lower)
            else ("r_safe_m", "m")
        )

    return VoiceConstraintResponse(
        scenario_id=target_scenario,
        parameter=param,
        value=num_val,
        unit=unit,
        summary=f"Parsed voice constraint: {target_scenario}.{param} = {num_val} {unit}",
        custom_spec_patch=f"Enforce {param}={num_val}{unit} on scenario {target_scenario}",
        source="deterministic-voice-parser",
    )
