#!/usr/bin/env python3
"""Live HTTP + SSE E2E smoke test against a running ProofForge 3D server."""

import argparse
import json
import sys

import httpx

EXPECTED_FRAMES = {
    "drone_swarm": (101, 42),
    "robot_arm": (41, 28),
    "spatial_tiling": (21, 18),
}


def parse_sse(text: str) -> list[tuple[str, dict]]:
    events: list[tuple[str, dict]] = []
    cur_event = "message"
    data_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("event:"):
            cur_event = line.split(":", 1)[1].strip()
        elif line.startswith("data:"):
            data_lines.append(line.split(":", 1)[1].strip())
        elif line == "":
            if data_lines:
                events.append((cur_event, json.loads("\n".join(data_lines))))
            cur_event = "message"
            data_lines = []
    if data_lines:
        events.append((cur_event, json.loads("\n".join(data_lines))))
    return events


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    parser.add_argument("--require-ui", action="store_true")
    args = parser.parse_args()
    base = args.base_url.rstrip("/")

    with httpx.Client(base_url=base, timeout=30.0) as client:
        health = client.get("/api/health")
        assert health.status_code == 200, f"/api/health HTTP {health.status_code}"
        h_json = health.json()
        assert h_json["status"] == "ok"
        assert h_json["mode"] == "deterministic"
        print(f"[SMOKE] /api/health OK: {h_json}")

        if args.require_ui or h_json.get("static_ui_ready"):
            ui = client.get("/")
            assert ui.status_code == 200, f"/ HTTP {ui.status_code}"
            assert "ProofForge 3D" in ui.text, "UI index.html missing ProofForge 3D title"
            print("[SMOKE] Static SPA UI (/) OK")

        for scenario_id, (exp_frames, exp_tick) in EXPECTED_FRAMES.items():
            run = client.post(
                "/api/forge/run",
                json={
                    "scenario_id": scenario_id,
                    "mode": "deterministic",
                    "inject_initial_bug": True,
                    "max_iterations": 5,
                    "enable_adversarial_hook_test": True,
                },
            )
            assert run.status_code == 200, f"run {scenario_id} failed: {run.text}"
            run_id = run.json()["runId"]

            stream = client.get(f"/api/forge/stream/{run_id}")
            assert stream.status_code == 200
            events = parse_sse(stream.text)

            hook_actions = [p.get("action") for ev, p in events if ev == "HOOK_AUDIT"]
            assert "BLOCKED" in hook_actions and "ALLOW" in hook_actions, hook_actions

            verifications = {p["phase"]: p for ev, p in events if ev == "VERIFICATION_RESULT"}
            assert verifications["before"]["result"]["status"] == "SAT_VIOLATION"
            assert verifications["before"]["result"]["violated_tick"] == exp_tick
            assert len(verifications["before"]["frames"]) == exp_frames

            assert verifications["after"]["result"]["status"] == "UNSAT_PROVEN"
            assert len(verifications["after"]["frames"]) == exp_frames

            diffs = [p.get("diff", "") for ev, p in events if ev == "PATCH_DIFF"]
            assert diffs and len(diffs[0]) > 20

            stages = [p.get("stage") for ev, p in events if ev == "STAGE_CHANGED"]
            assert stages[-1] == "COMPLETE", stages

            export = client.post(
                "/api/forge/export",
                json={
                    "scenario_id": scenario_id,
                    "result": verifications["after"]["result"],
                },
            )
            assert export.status_code == 200
            ex_json = export.json()
            assert ex_json["proxy_audit"]["redacted"] is True
            print(
                f"[SMOKE] {scenario_id}: SAT@{exp_tick} -> PATCH -> UNSAT "
                f"({exp_frames} frames, proxy export OK)"
            )

    print("SMOKE_E2E_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
