"""Protected Hook: reject writes outside workspace/impl/."""

import sys
from pathlib import Path

ALLOWED_PREFIX = Path("workspace/impl")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(2)
    target = Path(sys.argv[1])
    if ALLOWED_PREFIX not in target.parents and target != ALLOWED_PREFIX:
        print(f"HOOK_BLOCKED: write outside allowed scope ({target})")
        sys.exit(1)
    print(f"HOOK_ALLOW: {target}")
