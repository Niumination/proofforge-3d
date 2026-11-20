"""Pre-verify guard — cek SHA-256 invariants_locked.py sebelum Z3 jalan."""


def pre_verify_guard(expected_hash: str, content: str) -> bool:
    import hashlib

    return hashlib.sha256(content.encode()).hexdigest() == expected_hash
