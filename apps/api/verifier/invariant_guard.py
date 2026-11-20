"""Invariant guard — Phase 1: SHA-256 lock + anti-tamper (HOOK_AUDIT)."""


def compute_invariant_hash(content: str) -> str:
    import hashlib

    return hashlib.sha256(content.encode()).hexdigest()


def verify_hash(expected_hash: str, actual_content: str) -> bool:
    return compute_invariant_hash(actual_content) == expected_hash
