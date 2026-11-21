"""Isolated dynamic executor for synthesized Z3 bundles in custom-spec runs."""

import importlib.util
import sys
import tempfile
from pathlib import Path
from typing import Any

from apps.api.agents.argon_synth import CoGenBundle, validate_generated_python
from apps.api.verifier.invariant_guard import compute_invariant_hash


def execute_bundle(
    bundle: CoGenBundle,
    fixed: bool = False,
    timeout_ms: int = 8000,
) -> dict[str, Any]:
    """Write synthesized bundle to an isolated temp workspace, run Z3 check, and build 3D frames."""
    validate_generated_python(bundle.invariants_locked_py, "invariants_locked.py")
    validate_generated_python(bundle.system_impl_py, "system_impl.py")
    validate_generated_python(bundle.scene_adapter_py, "scene_adapter.py")

    inv_sha = compute_invariant_hash(bundle.invariants_locked_py)

    with tempfile.TemporaryDirectory(prefix="pf_synth_") as tmp:
        ws = Path(tmp)
        (ws / "invariants_locked.py").write_text(bundle.invariants_locked_py, encoding="utf-8")
        (ws / "system_impl.py").write_text(bundle.system_impl_py, encoding="utf-8")
        (ws / "scene_adapter.py").write_text(bundle.scene_adapter_py, encoding="utf-8")

        sys.path.insert(0, str(ws))
        loaded_mods: list[str] = []
        try:
            for mod_name in ("invariants_locked", "system_impl", "scene_adapter"):
                spec = importlib.util.spec_from_file_location(mod_name, ws / f"{mod_name}.py")
                assert spec and spec.loader
                mod = importlib.util.module_from_spec(spec)
                sys.modules[mod_name] = mod
                loaded_mods.append(mod_name)
                spec.loader.exec_module(mod)

            z3_out = sys.modules["system_impl"].run_z3_check(timeout_ms=timeout_ms)
            frames = sys.modules["scene_adapter"].build_timeline(fixed=fixed)
        finally:
            if str(ws) in sys.path:
                sys.path.remove(str(ws))
            for mod_name in loaded_mods:
                sys.modules.pop(mod_name, None)

    return {
        "invariant_sha256": inv_sha,
        "z3_result": z3_out,
        "frames": frames,
    }
