from pathlib import Path

from apps.api.main import app
from apps.api.verifier.invariant_guard import check_invariant_integrity, compute_file_hash
from apps.api.verifier.z3_runner import run_z3
from fastapi.testclient import TestClient


def test_drone_swarm_z3_sat_and_unsat() -> None:
    buggy = run_z3("drone_swarm", fixed=False)
    assert buggy["status"] == "SAT_VIOLATION"
    assert buggy["min_dist"] < 0.5
    assert buggy["violated_tick"] == 42

    fixed = run_z3("drone_swarm", fixed=True)
    assert fixed["status"] == "UNSAT_PROVEN"


def test_robot_arm_z3_sat_and_unsat() -> None:
    buggy = run_z3("robot_arm", fixed=False)
    assert buggy["status"] == "SAT_VIOLATION"
    assert buggy["tau2"] > 8.0

    fixed = run_z3("robot_arm", fixed=True)
    assert fixed["status"] == "UNSAT_PROVEN"


def test_spatial_tiling_z3_sat_and_unsat() -> None:
    buggy = run_z3("spatial_tiling", fixed=False)
    assert buggy["status"] == "SAT_VIOLATION"
    assert buggy["violated_tick"] == 18

    fixed = run_z3("spatial_tiling", fixed=True)
    assert fixed["status"] == "UNSAT_PROVEN"


def test_invariant_guard_blocks_tamper() -> None:
    inv = Path(__file__).resolve().parents[3] / "scenarios" / "drone_swarm" / "invariants_locked.py"
    expected = compute_file_hash(inv)
    valid, events = check_invariant_integrity(inv, expected, simulate_tamper=True)
    assert valid is True
    assert events[0]["action"] == "BLOCKED"
    assert events[1]["action"] == "ALLOW"


def test_api_health_forge_sse_and_export() -> None:
    client = TestClient(app)
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "ok"

    res_run = client.post(
        "/api/forge/run",
        json={
            "scenario_id": "drone_swarm",
            "mode": "deterministic",
            "inject_initial_bug": True,
            "max_iterations": 5,
            "enable_adversarial_hook_test": True,
        },
    )
    assert res_run.status_code == 200
    run_id = res_run.json()["runId"]

    res_stream = client.get(f"/api/forge/stream/{run_id}")
    assert res_stream.status_code == 200
    body = res_stream.text
    assert "event: HOOK_AUDIT" in body
    assert "BLOCKED" in body
    assert "event: VERIFICATION_RESULT" in body
    assert "SAT_VIOLATION" in body
    assert "UNSAT_PROVEN" in body
    assert "event: PATCH_DIFF" in body

    res_export = client.post(
        "/api/forge/export",
        json={
            "scenario_id": "drone_swarm",
            "result": {
                "iteration": 2,
                "status": "UNSAT_PROVEN",
                "invariant_hash_valid": True,
                "invariant_sha256": "abc123def456",
                "solver_duration_ms": 12,
            },
        },
    )
    assert res_export.status_code == 200
    assert res_export.json()["proxy_audit"]["redacted"] is True
