import json

import httpx
from apps.api.agents.argon_synth import ArgonCoGenerator, ArgonSynth, parse_voice_constraint_gemini
from apps.api.main import app
from fastapi.testclient import TestClient


def test_argon_synth_alias_and_gemini_voice_parser() -> None:
    assert ArgonSynth is ArgonCoGenerator

    def handler(req: httpx.Request) -> httpx.Response:
        assert "gemini-3.8-flash" in str(req.url)
        return httpx.Response(
            200,
            json={
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {
                                    "text": json.dumps(
                                        {
                                            "scenario_id": "drone_swarm",
                                            "parameter": "r_safe_m",
                                            "value": 2.4,
                                            "unit": "m",
                                            "summary": "Set drone_swarm.r_safe_m = 2.4 m",
                                        }
                                    )
                                }
                            ]
                        }
                    }
                ]
            },
        )

    out = parse_voice_constraint_gemini(
        "Increase drone separation to 2.4 meters",
        "drone_swarm",
        api_key="test-key",
        transport=httpx.MockTransport(handler),
    )
    assert out["value"] == 2.4
    assert out["parameter"] == "r_safe_m"


def test_certificate_endpoint_after_export() -> None:
    client = TestClient(app)
    res_export = client.post(
        "/api/forge/export",
        json={
            "scenario_id": "robot_arm",
            "result": {
                "iteration": 2,
                "status": "UNSAT_PROVEN",
                "invariant_hash_valid": True,
                "invariant_sha256": "deadbeef12345678",
                "solver_duration_ms": 9,
            },
        },
    )
    assert res_export.status_code == 200
    data = res_export.json()
    cert_res = client.get(f"/api/forge/certificate/{data['certificate_id']}")
    assert cert_res.status_code == 200
    assert cert_res.json()["certificate_digest_sha256"] == data["certificate_digest"]
    assert cert_res.json()["credential_exposed"] is False
