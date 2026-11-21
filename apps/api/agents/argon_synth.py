"""Gemini 4 Argon Co-Generator & Counterexample-Guided Patcher (`PF-020`)."""

import ast
import json
import re
from dataclasses import dataclass
from typing import Any

import httpx

from apps.api.agents.prompt_templates import (
    COGEN_SYSTEM_PROMPT,
    PATCH_SYSTEM_PROMPT,
    build_cogen_prompt,
    build_patch_prompt,
)
from apps.api.config import settings

FORBIDDEN_IMPORT_NODES = {"os", "subprocess", "socket", "shutil", "urllib", "requests", "httpx"}


@dataclass
class CoGenBundle:
    spec_summary: str
    invariants_locked_py: str
    system_impl_py: str
    scene_adapter_py: str
    patch_rationale: str
    source: str = "gemini-4-argon"


@dataclass
class PatchResult:
    patched_system_impl_py: str
    patch_rationale: str
    source: str = "gemini-4-argon"


def _strip_json_fences(raw: str) -> str:
    cleaned = raw.strip()
    fence = re.match(r"^```(?:json)?\s*(.*?)\s*```$", cleaned, flags=re.DOTALL)
    return fence.group(1).strip() if fence else cleaned


def validate_generated_python(code: str, filename: str = "<generated>") -> None:
    """Verify generated Python is syntactically valid and free of forbidden OS/network imports."""
    tree = ast.parse(code, filename=filename)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_mod = alias.name.split(".")[0]
                if root_mod in FORBIDDEN_IMPORT_NODES:
                    raise ValueError(f"Forbidden import in synthesized code: {root_mod}")
        elif isinstance(node, ast.ImportFrom) and node.module:
            root_mod = node.module.split(".")[0]
            if root_mod in FORBIDDEN_IMPORT_NODES:
                raise ValueError(f"Forbidden import-from in synthesized code: {root_mod}")
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"eval", "exec", "__import__", "open"}
        ):
                raise ValueError(f"Forbidden builtin call in synthesized code: {node.func.id}")


class ArgonCoGenerator:
    """Client for Gemini 4 Argon REST `generateContent` with strict JSON + AST validation."""

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        transport: httpx.BaseTransport | None = None,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
    ) -> None:
        self.api_key = api_key if api_key is not None else settings.gemini_api_key
        self.model = model or settings.gemini_frontier_model
        self.base_url = base_url.rstrip("/")
        self.transport = transport

    def _call_generate_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured for live_gemini mode")

        url = f"{self.base_url}/models/{self.model}:generateContent"
        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "temperature": 0.15,
                "responseMimeType": "application/json",
            },
        }
        client_kwargs: dict[str, Any] = {"timeout": 45.0}
        if self.transport is not None:
            client_kwargs["transport"] = self.transport

        with httpx.Client(**client_kwargs) as client:
            resp = client.post(
                url,
                headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
                json=payload,
            )
            resp.raise_for_status()
            body = resp.json()

        candidates = body.get("candidates") or []
        if not candidates:
            raise RuntimeError(f"Gemini returned empty candidates: {body}")
        text = candidates[0]["content"]["parts"][0]["text"]
        return json.loads(_strip_json_fences(text))

    def synthesize_bundle(self, custom_spec: str, inject_bug: bool = True) -> CoGenBundle:
        data = self._call_generate_json(
            COGEN_SYSTEM_PROMPT, build_cogen_prompt(custom_spec, inject_bug=inject_bug)
        )
        for key in ("invariants_locked_py", "system_impl_py", "scene_adapter_py"):
            if key not in data or not isinstance(data[key], str):
                raise ValueError(f"Missing required bundle field: {key}")
            validate_generated_python(data[key], filename=key)

        return CoGenBundle(
            spec_summary=str(data.get("spec_summary", custom_spec[:120])),
            invariants_locked_py=data["invariants_locked_py"],
            system_impl_py=data["system_impl_py"],
            scene_adapter_py=data["scene_adapter_py"],
            patch_rationale=str(data.get("patch_rationale", "")),
        )

    def patch_from_counterexample(
        self,
        system_impl_py: str,
        invariants_locked_py: str,
        counterexample: dict[str, Any],
        violated_invariant: str | None,
    ) -> PatchResult:
        data = self._call_generate_json(
            PATCH_SYSTEM_PROMPT,
            build_patch_prompt(
                system_impl_py=system_impl_py,
                invariants_locked_py=invariants_locked_py,
                counterexample=counterexample,
                violated_invariant=violated_invariant,
            ),
        )
        patched = data.get("patched_system_impl_py", "")
        if not isinstance(patched, str) or not patched.strip():
            raise ValueError("Missing patched_system_impl_py in Gemini patch response")
        validate_generated_python(patched, filename="patched_system_impl.py")
        return PatchResult(
            patched_system_impl_py=patched,
            patch_rationale=str(data.get("patch_rationale", "Surgical counterexample patch applied.")),
        )


ArgonSynth = ArgonCoGenerator


def parse_voice_constraint_gemini(
    transcript: str,
    scenario_id: str,
    api_key: str | None = None,
    model: str | None = None,
    transport: httpx.BaseTransport | None = None,
) -> dict[str, Any]:
    """Use gemini-3.8-flash JSON mode to extract structured constraint edits from voice text."""
    key = api_key if api_key is not None else settings.gemini_api_key
    mdl = model or settings.gemini_fast_model
    if not key:
        raise RuntimeError("GEMINI_API_KEY not configured")

    prompt = (
        f"Extract a single verification constraint edit from transcript: {transcript!r}. "
        f"Default scenario_id: {scenario_id}. Return JSON with keys: "
        "scenario_id (drone_swarm|robot_arm|spatial_tiling), parameter, value (number), unit, summary."
    )
    gen = ArgonCoGenerator(api_key=key, model=mdl, transport=transport)
    return gen._call_generate_json(
        "Return strict JSON only for ProofForge 3D constraint extraction.", prompt
    )
