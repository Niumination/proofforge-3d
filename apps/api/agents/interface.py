from abc import ABC, abstractmethod
from typing import Any


class AgentRunnerInterface(ABC):
    @abstractmethod
    def run_pipeline(
        self,
        scenario_id: str,
        inject_initial_bug: bool,
        enable_adversarial_hook_test: bool,
    ) -> dict[str, Any]:
        raise NotImplementedError
