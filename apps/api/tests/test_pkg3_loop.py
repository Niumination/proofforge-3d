import json

import httpx
from apps.api.agents.argon_synth import ArgonCoGenerator
from apps.api.agents.closed_loop import ClosedLoopOrchestrator
from apps.api.main import app
from fastapi.testclient import TestClient


def test_closed_loop_live_mock_converges_sat_to_unsat() -> None:
    calls = {"n": 0}

    def handler(req: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        if calls["n"] == 1:
            payload = {
                "spec_summary": "Corridor clearance >= 2m",
                "invariants_locked_py": "SAFE_GAP = 2\n",
                "system_impl_py": (
                    "from z3 import Int, Solver, sat\n"
                    "from invariants_locked import SAFE_GAP\n"
                    "def run_z3_check(timeout_ms: int = 8000) -> dict:\n"
                    "    s = Solver(); g = Int('g'); s.add(g == 1, g < SAFE_GAP)\n"
                    "    if s.check() == sat:\n"
                    "        return {'status': 'SAT_VIOLATION', 'violated_tick': 2, "
                    "'violated_time_sec': 0.2, 'solver_duration_ms': 1, "
                    "'violated_invariant': 'g >= 2', 'counterexample_inputs': {'g': 1}}\n"
                    "    return {'status': 'UNSAT_PROVEN'}\n"
                ),
                "scene_adapter_py": (
                    "def build_timeline(fixed: bool) -> list[dict]:\n"
                    "    return [{'tick': 0, 'time_sec': 0.0, 'is_violation': not fixed, "
                    "'entities': [], 'constraints_overlay': []}]\n"
                ),
                "patch_rationale": "Buggy initial spacing",
            }
        else:
            payload = {
                "patched_system_impl_py": (
                    "from z3 import Int, Solver, sat\n"
                    "from invariants_locked import SAFE_GAP\n"
                    "def run_z3_check(timeout_ms: int = 8000) -> dict:\n"
                    "    s = Solver(); g = Int('g'); s.add(g >= SAFE_GAP, g < SAFE_GAP)\n"
                    "    if s.check() == sat:\n"
                    "        return {'status': 'SAT_VIOLATION'}\n"
                    "    return {'status': 'UNSAT_PROVEN', 'violated_tick': None, "
                    "'violated_time_sec': None, 'solver_duration_ms': 2, "
                    "'violated_invariant': None, 'counterexample_inputs': None}\n"
                ),
                "patch_rationale": "Enforced g >= SAFE_GAP",
            }
        return httpx.Response(
            200,
            json={"candidates": [{"content": {"parts": [{"text": json.dumps(payload)}]}}]},
        )

    argon = ArgonCoGenerator(api_key="test-key", transport=httpx.MockTransport(handler))
    orch = ClosedLoopOrchestrator(argon=argon)
    out = orch.run(
        scenario_id="drone_swarm",
        mode="live_gemini",
        custom_spec="Keep corridor gap >= 2m",
        inject_initial_bug=True,
        max_iterations=3,
    )
    assert len(out["iterations"]) == 2
    assert out["iterations"][0]["result"]["status"] == "SAT_VIOLATION"
    assert out["iterations"][1]["result"]["status"] == "UNSAT_PROVEN"
    assert out["certificate"]["verification_status"] == "UNSAT_PROVEN"
    assert "system_impl_before.py" in out["patch_diff"]


def test_redteam_and_voice_constraint_endpoints() -> None:
    client = TestClient(app)

    rt = client.post("/api/forge/redteam", json={"scenario_id": "drone_swarm"})
    assert rt.status_code == 200
    rt_json = rt.json()
    assert rt_json["all_blocked"] is True
    assert rt_json["blocked_count"] >= 3

    vc = client.post(
        "/api/forge/voice-constraint",
        json={"transcript": "Limit robot arm payload to 3.0 kg", "scenario_id": "drone_swarm"},
    )
    assert vc.status_code == 200
    vc_json = vc.json()
    assert vc_json["scenario_id"] == "robot_arm"
    assert vc_json["parameter"] == "payload_kg"
    assert vc_json["value"] == 3.0

    run = client.post(
        "/api/forge/run",
        json={
            "scenario_id": "drone_swarm",
            "mode": "live_gemini",
            "inject_initial_bug": True,
            "simulate_prompt_injection": True,
        },
    )
    assert run.status_code == 200
    stream = client.get(f"/api/forge/stream/{run.json()['runId']}")
    assert stream.status_code == 200
    assert "PROOF_CERTIFICATE" in stream.text
    assert "BLOCKED" in stream.text
