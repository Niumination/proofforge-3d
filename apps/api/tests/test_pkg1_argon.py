import json

import httpx
import pytest
from apps.api.agents.argon_synth import ArgonCoGenerator, validate_generated_python
from apps.api.verifier.dynamic_runner import execute_bundle


def _mock_gemini_response(payload_dict: dict) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers.get("x-goog-api-key") == "test-key"
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {"content": {"parts": [{"text": json.dumps(payload_dict)}]}}
                ]
            },
        )

    return httpx.MockTransport(handler)


def test_argon_cogenerator_synthesizes_and_executes_z3_bundle() -> None:
    fake_bundle = {
        "spec_summary": "1D corridor safe distance >= 2m",
        "invariants_locked_py": "SAFE_GAP = 2\n",
        "system_impl_py": (
            "from z3 import Int, Solver, sat, unsat\n"
            "from invariants_locked import SAFE_GAP\n"
            "def run_z3_check(timeout_ms: int = 8000) -> dict:\n"
            "    s = Solver(); s.set('timeout', timeout_ms)\n"
            "    gap = Int('gap')\n"
            "    s.add(gap == 1)\n"
            "    s.add(gap < SAFE_GAP)\n"
            "    if s.check() == sat:\n"
            "        return {'status': 'SAT_VIOLATION', 'violated_tick': 3, "
            "'violated_time_sec': 0.3, 'solver_duration_ms': 1, "
            "'violated_invariant': 'gap >= 2', 'counterexample_inputs': {'gap': 1}}\n"
            "    return {'status': 'UNSAT_PROVEN', 'violated_tick': None, "
            "'violated_time_sec': None, 'solver_duration_ms': 1, "
            "'violated_invariant': None, 'counterexample_inputs': None}\n"
        ),
        "scene_adapter_py": (
            "def build_timeline(fixed: bool) -> list[dict]:\n"
            "    return [{'tick': 0, 'time_sec': 0.0, 'is_violation': not fixed, "
            "'entities': [], 'constraints_overlay': []}]\n"
        ),
        "patch_rationale": "Initial naive gap=1 violates SAFE_GAP=2",
    }

    gen = ArgonCoGenerator(api_key="test-key", transport=_mock_gemini_response(fake_bundle))
    bundle = gen.synthesize_bundle("Keep 2m corridor gap", inject_bug=True)
    out = execute_bundle(bundle, fixed=False)
    assert out["z3_result"]["status"] == "SAT_VIOLATION"
    assert out["frames"][0]["is_violation"] is True


def test_argon_patch_from_counterexample_returns_valid_code() -> None:
    patch_resp = {
        "patched_system_impl_py": (
            "from z3 import Int, Solver, sat\n"
            "from invariants_locked import SAFE_GAP\n"
            "def run_z3_check(timeout_ms: int = 8000) -> dict:\n"
            "    s = Solver(); gap = Int('gap'); s.add(gap >= SAFE_GAP, gap < SAFE_GAP)\n"
            "    if s.check() == sat:\n"
            "        return {'status': 'SAT_VIOLATION'}\n"
            "    return {'status': 'UNSAT_PROVEN', 'violated_tick': None, "
            "'violated_time_sec': None, 'solver_duration_ms': 1, "
            "'violated_invariant': None, 'counterexample_inputs': None}\n"
        ),
        "patch_rationale": "Clamped gap >= SAFE_GAP",
    }
    gen = ArgonCoGenerator(api_key="test-key", transport=_mock_gemini_response(patch_resp))
    patched = gen.patch_from_counterexample(
        "gap = 1", "SAFE_GAP = 2", {"gap": 1}, "gap >= 2"
    )
    assert "UNSAT_PROVEN" in patched.patched_system_impl_py


def test_ast_guard_blocks_unsafe_imports_and_builtins() -> None:
    with pytest.raises(ValueError, match="Forbidden import"):
        validate_generated_python("import subprocess\nsubprocess.run(['ls'])")
    with pytest.raises(ValueError, match="Forbidden builtin"):
        validate_generated_python("eval('1+1')")
