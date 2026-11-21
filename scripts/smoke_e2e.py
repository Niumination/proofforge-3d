#!/usr/bin/env python3
"""Live HTTP + SSE E2E smoke test covering Phase 1-3 endpoints against a running ProofForge 3D server."""

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
        print(f"[SMOKE] /api/health OK: {h_json}")

        if args.require_ui or h_json.get("static_ui_ready"):
            ui = client.get("/")
            assert ui.status_code == 200, f"/ HTTP {ui.status_code}"
            assert "ProofForge 3D" in ui.text
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
            assert run.status_code == 200
            run_id = run.json()["runId"]

            stream = client.get(f"/api/forge/stream/{run_id}")
            assert stream.status_code == 200
            events = parse_sse(stream.text)

            hook_actions = [p.get("action") for ev, p in events if ev == "HOOK_AUDIT"]
            assert "BLOCKED" in hook_actions and "ALLOW" in hook_actions

            verifications = {p["phase"]: p for ev, p in events if ev == "VERIFICATION_RESULT"}
            assert verifications["before"]["result"]["status"] == "SAT_VIOLATION"
            assert verifications["before"]["result"]["violated_tick"] == exp_tick
            assert len(verifications["before"]["frames"]) == exp_frames
            assert verifications["after"]["result"]["status"] == "UNSAT_PROVEN"

            certs = [p for ev, p in events if ev == "PROOF_CERTIFICATE"]
            assert certs and certs[0]["verification_status"] == "UNSAT_PROVEN"

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

            cert_get = client.get(f"/api/forge/certificate/{ex_json['certificate_id']}")
            assert cert_get.status_code == 200
            assert cert_get.json()["certificate_digest_sha256"] == ex_json["certificate_digest"]
            print(
                f"[SMOKE] {scenario_id}: SAT@{exp_tick} -> PATCH -> UNSAT "
                f"({exp_frames} frames, cert={ex_json['certificate_id']} OK)"
            )

        rt = client.post("/api/forge/redteam", json={"scenario_id": "drone_swarm"})
        assert rt.status_code == 200 and rt.json()["all_blocked"] is True
        print(f"[SMOKE] /api/forge/redteam OK (blocked={rt.json()['blocked_count']})")

        vc = client.post(
            "/api/forge/voice-constraint",
            json={"transcript": "Set drone separation to 2.2 meters", "scenario_id": "drone_swarm"},
        )
        assert vc.status_code == 200 and vc.json()["value"] == 2.2
        print(f"[SMOKE] /api/forge/voice-constraint OK ({vc.json()['summary']})")

    print("SMOKE_E2E_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
