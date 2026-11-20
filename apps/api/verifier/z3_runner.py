"""Z3 runner — Phase 1: deterministic subprocess runner dengan timeout (8000 ms)."""


def run_z3(scenario: str, timeout_ms: int = 8000) -> dict:
    # Phase 1: dipanggil dari deterministic_sim / scenario impl
    return {"scenario": scenario, "status": "ERROR", "solver_duration_ms": timeout_ms}
