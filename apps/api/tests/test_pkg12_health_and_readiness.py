from apps.api.main import app
from fastapi.testclient import TestClient


def test_health_exposes_stage_readiness_metadata() -> None:
    client = TestClient(app)
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert isinstance(data["gemini_key_configured"], bool)
    assert data["frontier_model"] == "gemini-4-argon"
    assert data["managed_agent_id"] == "antigravity-preview-09-2026"
    assert data["scenarios_count"] == 3
