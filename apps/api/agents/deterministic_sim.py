"""Deterministic simulator — Phase 1: mesin verifikasi lokal (tanpa API AI eksternal)."""


class DeterministicSim:
    def __init__(self) -> None:
        self.timeline: list[dict] = []

    def run_scenario(self, scenario_id: str, inject_initial_bug: bool) -> dict:
        # Phase 1: deterministic — akan dipanggil oleh orchestrator PF-007
        return {"scenario_id": scenario_id, "frames": self.timeline}
