"""Write scope guard — tolak penulisan di luar workspace/impl/ dan workspace/skills/."""


def write_scope_guard(path: str, allowed_prefixes: tuple[str, ...] = ("workspace/impl/", "workspace/skills/")) -> bool:
    return path.startswith(allowed_prefixes)
