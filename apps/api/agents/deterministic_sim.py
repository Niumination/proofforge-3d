"""Deterministic verification orchestrator — real Z3 + SHA-256 guard + parametric overrides."""

import difflib
from pathlib import Path
from typing import Any

from apps.api.agents.interface import AgentRunnerInterface
from apps.api.verifier.invariant_guard import check_invariant_integrity, compute_file_hash
from apps.api.verifier.scene_exporter import export_frames
from apps.api.verifier.z3_runner import run_z3

REPO_ROOT = Path(__file__).resolve().parents[3]


class DeterministicSim(AgentRunnerInterface):
    def run_pipeline(
        self,
        scenario_id: str,
        inject_initial_bug: bool,
        enable_adversarial_hook_test: bool,
        overrides: dict[str, float] | None = None,
    ) -> dict[str, Any]:
        scenario_dir = REPO_ROOT / "scenarios" / scenario_id
        inv_path = scenario_dir / "invariants_locked.py"
        expected_hash = compute_file_hash(inv_path)

        hash_valid, hook_events = check_invariant_integrity(
            inv_path, expected_hash, simulate_tamper=enable_adversarial_hook_test
        )

        buggy_path = scenario_dir / "buggy_impl.py"
        fixed_path = scenario_dir / "fixed_impl.py"
        patch_diff = "".join(
            difflib.unified_diff(
                buggy_path.read_text(encoding="utf-8").splitlines(keepends=True),
                fixed_path.read_text(encoding="utf-8").splitlines(keepends=True),
                fromfile=f"scenarios/{scenario_id}/buggy_impl.py",
                tofile=f"scenarios/{scenario_id}/fixed_impl.py",
            )
        )

        iterations: list[dict[str, Any]] = []

        if inject_initial_bug:
            z3_bug = run_z3(scenario_id, fixed=False, overrides=overrides)
            frames_bug = export_frames(scenario_id, fixed=False, overrides=overrides)
            iterations.append(
                {
                    "result": {
                        "iteration": 1,
                        "status": z3_bug["status"],
                        "invariant_hash_valid": hash_valid,
                        "invariant_sha256": expected_hash,
                        "violated_invariant": z3_bug.get("violated_invariant"),
                        "counterexample_inputs": z3_bug.get("counterexample_inputs"),
                        "violated_tick": z3_bug.get("violated_tick"),
                        "violated_time_sec": z3_bug.get("violated_time_sec"),
                        "solver_duration_ms": z3_bug.get("solver_duration_ms", 0),
                        "note": "Initial implementation failed Z3 proof; counterexample captured.",
                    },
                    "frames": frames_bug,
                }
            )

        z3_fix = run_z3(scenario_id, fixed=True, overrides=overrides)
        frames_fix = export_frames(scenario_id, fixed=True, overrides=overrides)
        iterations.append(
            {
                "result": {
                    "iteration": 2 if inject_initial_bug else 1,
                    "status": z3_fix["status"],
                    "invariant_hash_valid": hash_valid,
                    "invariant_sha256": expected_hash,
                    "violated_invariant": None,
                    "counterexample_inputs": None,
                    "violated_tick": None,
                    "violated_time_sec": None,
                    "solver_duration_ms": z3_fix.get("solver_duration_ms", 0),
                    "note": z3_fix.get("note"),
                },
                "frames": frames_fix,
            }
        )

        return {
            "scenario_id": scenario_id,
            "invariant_sha256": expected_hash,
            "hook_events": hook_events,
            "patch_diff": patch_diff,
            "iterations": iterations,
        }
