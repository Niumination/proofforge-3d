"""Invariant guard — SHA-256 lock & anti-tamper verification (HOOK_AUDIT)."""

import hashlib
from pathlib import Path
from typing import Any


def compute_invariant_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def compute_file_hash(file_path: Path) -> str:
    return compute_invariant_hash(file_path.read_text(encoding="utf-8"))


def verify_hash(expected_hash: str, actual_content: str) -> bool:
    return compute_invariant_hash(actual_content) == expected_hash


def check_invariant_integrity(
    invariant_path: Path,
    expected_hash: str,
    simulate_tamper: bool = False,
) -> tuple[bool, list[dict[str, Any]]]:
    """Verify invariant file integrity and optionally simulate a Protected Hook block."""
    events: list[dict[str, Any]] = []
    actual_content = invariant_path.read_text(encoding="utf-8")
    actual_hash = compute_invariant_hash(actual_content)

    if simulate_tamper:
        tampered_preview = actual_content + "\n# TAMPERED: relax safety threshold\n"
        tampered_hash = compute_invariant_hash(tampered_preview)
        events.append(
            {
                "action": "BLOCKED",
                "hook": "pre_verify_invariant_guard",
                "target": str(invariant_path.name),
                "expected_sha256": expected_hash[:16],
                "attempted_sha256": tampered_hash[:16],
                "reason": "Immutable invariant contract SHA-256 mismatch prevented by Protected Hook",
            }
        )

    is_valid = actual_hash == expected_hash
    events.append(
        {
            "action": "ALLOW" if is_valid else "BLOCKED",
            "hook": "pre_verify_invariant_guard",
            "target": str(invariant_path.name),
            "expected_sha256": expected_hash[:16],
            "actual_sha256": actual_hash[:16],
            "reason": "Invariant SHA-256 verified intact" if is_valid else "Invariant modified on disk",
        }
    )
    return is_valid, events
