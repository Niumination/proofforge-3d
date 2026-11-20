"""Managed runner — Phase 3: Google Managed Agents client (antigravity)."""


class ManagedRunner:
    def __init__(self, agent_id: str) -> None:
        self.agent_id = agent_id

    def run(self, *args, **kwargs):
        raise NotImplementedError("Phase 3: managed agents execution")
