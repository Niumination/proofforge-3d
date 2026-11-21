"""Antigravity Managed Agents sandbox runner (`PF-021`) with local subprocess parity."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import httpx

from apps.api.config import settings
from apps.api.security.protected_hooks import evaluate_invariant_patch_attempt
from apps.api.verifier.invariant_guard import compute_invariant_hash


class ManagedAgentRunner:
    """Executes verification inside `antigravity-preview-09-2026` or isolated local subprocess."""

    def __init__(
        self,
        api_key: str | None = None,
        agent_id: str | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.api_key = api_key if api_key is not None else settings.gemini_api_key
        self.agent_id = agent_id or settings.gemini_managed_agent_id
        self.transport = transport

    def run_local_sandbox(
        self,
        invariants_locked_py: str,
        system_impl_py: str,
        baseline_sha256: str,
        timeout_sec: int = 12,
    ) -> dict[str, Any]:
        hook_ev = evaluate_invariant_patch_attempt(baseline_sha256, invariants_locked_py)
        if hook_ev["action"] != "ALLOW":
            return {"hook_audit": hook_ev, "z3_result": {"status": "ERROR"}, "blocked": True}

        with tempfile.TemporaryDirectory(prefix="pf_sandbox_") as tmp:
            ws = Path(tmp)
            (ws / "invariants_locked.py").write_text(invariants_locked_py, encoding="utf-8")
            (ws / "system_impl.py").write_text(system_impl_py, encoding="utf-8")
            driver = (
                "import json, system_impl\n"
                "print(json.dumps(system_impl.run_z3_check()))\n"
            )
            proc = subprocess.run(
                [sys.executable, "-c", driver],
                cwd=ws,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                check=False,
            )
            if proc.returncode != 0:
                raise RuntimeError(f"Sandbox execution failed: {proc.stderr.strip()}")
            z3_out = json.loads(proc.stdout.strip().splitlines()[-1])

        return {
            "hook_audit": hook_ev,
            "z3_result": z3_out,
            "impl_sha256": compute_invariant_hash(system_impl_py),
            "blocked": False,
            "sandbox_runtime": "local-subprocess-sandbox",
        }

    def execute_remote_interaction(self, prompt: str) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY required for remote Managed Agent interaction")

        url = "https://generativelanguage.googleapis.com/v1beta/interactions"
        payload = {
            "model": self.agent_id,
            "input": prompt,
        }
        kwargs: dict[str, Any] = {"timeout": 45.0}
        if self.transport is not None:
            kwargs["transport"] = self.transport

        with httpx.Client(**kwargs) as client:
            res = client.post(
                url,
                headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
                json=payload,
            )
            res.raise_for_status()
            return res.json()
