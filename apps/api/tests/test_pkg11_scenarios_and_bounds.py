from apps.api.main import app
from apps.api.routes import forge as forge_routes
from fastapi.testclient import TestClient


def test_scenarios_catalog_endpoint() -> None:
    client = TestClient(app)
    res = client.get("/api/forge/scenarios")
    assert res.status_code == 200
    ids = {s["id"] for s in res.json()["scenarios"]}
    assert ids == {"drone_swarm", "robot_arm", "spatial_tiling"}


def test_runs_store_bounded_eviction() -> None:
    forge_routes._runs.clear()
    client = TestClient(app)
    for i in range(forge_routes.MAX_STORED_RUNS + 5):
        forge_routes._runs[f"synthetic-{i}"] = {"idx": i}
    res = client.post(
        "/api/forge/run",
        json={"scenario_id": "spatial_tiling", "mode": "deterministic"},
    )
    assert res.status_code == 200
    assert len(forge_routes._runs) <= forge_routes.MAX_STORED_RUNS
    assert client.get("/api/forge/stream/synthetic-0").status_code == 404
