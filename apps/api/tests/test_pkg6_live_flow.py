import json

import httpx
from apps.api.agents.argon_synth import ArgonCoGenerator
from apps.api.agents.closed_loop import ClosedLoopOrchestrator


def test_live_gemini_autoloads_scenario_spec_when_custom_spec_empty() -> None:
    def handler(req: httpx.Request) -> httpx.Response:
        body = json.loads(req.content.decode("utf-8"))
        user_txt = body["contents"][0]["parts"][0]["text"]
        assert "Drone" in user_txt or "R_SAFE" in user_txt or "1.5" in user_txt
        payload = {
            "spec_summary": "Auto-loaded drone_swarm spec",
            "invariants_locked_py": "SAFE_GAP = 2\n",
            "system_impl_py": (
                "from z3 import Int, Solver, sat\n"
                "from invariants_locked import SAFE_GAP\n"
                "def run_z3_check(timeout_ms: int = 8000) -> dict:\n"
                "    s = Solver(); g = Int('g'); s.add(g >= SAFE_GAP, g < SAFE_GAP)\n"
                "    if s.check() == sat:\n"
                "        return {'status': 'SAT_VIOLATION'}\n"
                "    return {'status': 'UNSAT_PROVEN', 'violated_tick': None, "
                "'violated_time_sec': None, 'solver_duration_ms': 1, "
                "'violated_invariant': None, 'counterexample_inputs': None}\n"
            ),
            "scene_adapter_py": (
                "def build_timeline(fixed: bool) -> list[dict]:\n"
                "    return [{'tick': 0, 'time_sec': 0.0, 'is_violation': False, "
                "'entities': [], 'constraints_overlay': []}]\n"
            ),
            "patch_rationale": "Direct safe synthesis",
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
        custom_spec="",
        inject_initial_bug=False,
    )
    assert out["iterations"][0]["result"]["status"] == "UNSAT_PROVEN"
    assert out["certificate"]["verification_status"] == "UNSAT_PROVEN"


def test_deterministic_override_propagates_to_result_note() -> None:
    orch = ClosedLoopOrchestrator()
    out = orch.run(
        scenario_id="drone_swarm",
        mode="deterministic",
        custom_spec="Enforce r_safe_m=2.2m on scenario drone_swarm",
        inject_initial_bug=True,
    )
    last_note = out["iterations"][-1]["result"]["note"]
    assert "r_safe_m=2.2m" in last_note
