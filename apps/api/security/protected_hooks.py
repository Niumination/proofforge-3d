"""Protected Hooks engine (`PF-022`) — blocks invariant tampering, out-of-scope writes, and prompt injection."""

import re
from pathlib import Path
from typing import Any

from apps.api.verifier.invariant_guard import compute_invariant_hash

INJECTION_PATTERNS = [
    (re.compile(r"invariants_locked\.py", re.IGNORECASE), "Attempted reference/modification of locked invariant file"),
    (re.compile(r"(ignore|bypass|disable|skip)\s+(z3|invariant|safety|hook)", re.IGNORECASE), "Adversarial bypass directive detected"),
    (re.compile(r"(weaken|relax|lower|set)\s+(r_safe|tau_max|safety)", re.IGNORECASE), "Reward-hacking threshold relaxation attempt"),
    (re.compile(r"(gemini_api_key|github_token|ghp_|os\.environ|secrets)", re.IGNORECASE), "Credential exfiltration attempt blocked"),
]

SECRET_SCRUB_PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z\-_]{20,}"),
    re.compile(r"ghp_[0-9A-Za-z]{20,}"),
    re.compile(r"github_pat_[0-9A-Za-z_]{20,}"),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9\-._~+/]+=*"),
]


def redact_secrets(text: str) -> str:
    cleaned = text
    for pat in SECRET_SCRUB_PATTERNS:
        cleaned = pat.sub("[REDACTED_CREDENTIAL]", cleaned)
    return cleaned


def evaluate_write_scope(target_path: str) -> dict[str, Any]:
    norm = Path(target_path).as_posix().lstrip("./")
    blocked_markers = ("invariants_locked", ".env", ".git/", "secrets/", "/etc/")
    if any(m in norm for m in blocked_markers) or norm.startswith("/"):
        return {
            "action": "BLOCKED",
            "hook": "write_scope_guard",
            "target": target_path,
            "reason": "Write target violates Protected Hook workspace/impl boundary",
        }
    allowed_prefixes = ("workspace/impl/", "scenarios/", "system_impl.py")
    if norm.startswith(allowed_prefixes) or norm == "system_impl.py":
        return {
            "action": "ALLOW",
            "hook": "write_scope_guard",
            "target": target_path,
            "reason": "Target inside mutable implementation scope",
        }
    return {
        "action": "BLOCKED",
        "hook": "write_scope_guard",
        "target": target_path,
        "reason": "Target outside explicit impl allowlist",
    }


def evaluate_invariant_patch_attempt(
    baseline_sha256: str,
    candidate_content: str,
    target_name: str = "invariants_locked.py",
) -> dict[str, Any]:
    candidate_sha = compute_invariant_hash(candidate_content)
    if candidate_sha != baseline_sha256:
        return {
            "action": "BLOCKED",
            "hook": "pre_verify_invariant_guard",
            "target": target_name,
            "expected_sha256": baseline_sha256[:16],
            "attempted_sha256": candidate_sha[:16],
            "reason": "Immutable Z3 invariant SHA-256 mismatch blocked by Protected Hook",
        }
    return {
        "action": "ALLOW",
        "hook": "pre_verify_invariant_guard",
        "target": target_name,
        "expected_sha256": baseline_sha256[:16],
        "actual_sha256": candidate_sha[:16],
        "reason": "Invariant SHA-256 verified intact",
    }


def detect_prompt_injection(spec_or_prompt: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for regex, reason in INJECTION_PATTERNS:
        if regex.search(spec_or_prompt):
            events.append(
                {
                    "action": "BLOCKED",
                    "hook": "red_team_prompt_guard",
                    "target": "agent_prompt",
                    "reason": reason,
                    "excerpt": redact_secrets(spec_or_prompt[:100]),
                }
            )
    return events
