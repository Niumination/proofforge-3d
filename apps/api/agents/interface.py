"""AgentRunner interface — Phase 1: memisahkan deterministic vs live (Phase 3)."""


class AgentRunner:
    def __init__(self, mode: str) -> None:
        self.mode = mode

    def run(self, *args, **kwargs):
        raise NotImplementedError("Phase 1: deterministic_sim; Phase 3: argon_synth/managed_runner")
