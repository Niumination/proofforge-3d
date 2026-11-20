"""Protected Hook: verify SHA-256 integrity of invariants_locked.py before verification."""

import hashlib
import sys
from pathlib import Path


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pre_verify_guard.py <invariants_path> <expected_sha256>")
        sys.exit(2)
    actual = sha256_file(Path(sys.argv[1]))
    if actual != sys.argv[2]:
        print(f"HOOK_BLOCKED: hash mismatch ({actual} != {sys.argv[2]})")
        sys.exit(1)
    print(f"HOOK_ALLOW: {actual}")
