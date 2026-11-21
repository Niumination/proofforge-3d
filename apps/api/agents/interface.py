"""Abstract verification engine interface shared by deterministic & live Gemini 4 Argon runners."""

from abc import ABC, abstractmethod
from typing import Any


class AgentRunnerInterface(ABC):
    @abstractmethod
    def run_pipeline(
        self,
        scenario_id: str,
        inject_initial_bug: bool = True,
        enable_adversarial_hook_test: bool = True,
    ) -> dict[str, Any]:
        """Execute verification pipeline and return structured frames, Z3 results, and audit logs."""


VerificationAgentInterface = AgentRunnerInterface
