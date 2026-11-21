from apps.api.agents.closed_loop import ClosedLoopOrchestrator
from apps.api.verifier.scene_exporter import export_frames
from apps.api.verifier.z3_runner import parse_constraint_overrides, run_z3


def test_parse_and_apply_drone_r_safe_override() -> None:
    ov = parse_constraint_overrides("Enforce r_safe_m=2.2m on scenario drone_swarm")
    assert ov == {"r_safe_m": 2.2}

    fixed = run_z3("drone_swarm", fixed=True, overrides=ov)
    assert fixed["status"] == "UNSAT_PROVEN"

    frames = export_frames("drone_swarm", fixed=True, overrides=ov)
    assert frames[0]["constraints_overlay"][0]["radius"] == 2.2


def test_robot_arm_payload_override_updates_z3_and_3d_telemetry() -> None:
    orch = ClosedLoopOrchestrator()
    out = orch.run(
        scenario_id="robot_arm",
        mode="deterministic",
        custom_spec="Enforce payload_kg=3.0kg on scenario robot_arm",
        inject_initial_bug=True,
    )
    bug_res = out["iterations"][0]["result"]
    assert bug_res["counterexample_inputs"]["m_payload_kg"] == 3.0
    assert out["iterations"][-1]["result"]["status"] == "UNSAT_PROVEN"
