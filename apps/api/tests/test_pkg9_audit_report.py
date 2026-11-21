from apps.api.main import app
from fastapi.testclient import TestClient


def test_markdown_audit_report_download_and_404() -> None:
    client = TestClient(app)
    assert client.get("/api/forge/report/cert-missing").status_code == 404

    exp = client.post(
        "/api/forge/export",
        json={
            "scenario_id": "spatial_tiling",
            "result": {
                "iteration": 2,
                "status": "UNSAT_PROVEN",
                "invariant_hash_valid": True,
                "invariant_sha256": "cafe1234deadbeef",
                "solver_duration_ms": 7,
            },
        },
    )
    assert exp.status_code == 200
    cert_id = exp.json()["certificate_id"]

    rep = client.get(f"/api/forge/report/{cert_id}")
    assert rep.status_code == 200
    assert "text/markdown" in rep.headers["content-type"]
    assert "UNSAT_PROVEN" in rep.text
    assert cert_id in rep.text
