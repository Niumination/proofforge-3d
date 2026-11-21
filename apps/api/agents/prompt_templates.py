"""Prompt templates for Gemini 4 Argon Co-Generation & Surgical Self-Patching."""

COGEN_SYSTEM_PROMPT = """You are ProofForge 3D's formal co-generator powered by Gemini 4 Argon.
Given a physical or concurrency system specification, emit STRICT JSON with exactly 5 string keys:
- "spec_summary": concise technical summary of the system and safety invariant
- "invariants_locked_py": immutable Z3 safety condition helper (NO sqrt/sin/cos; pure QF_LIA or quadratic polynomials)
- "system_impl_py": Python module exposing `run_z3_check(timeout_ms: int = 8000) -> dict` returning status "SAT_VIOLATION" or "UNSAT_PROVEN"
- "scene_adapter_py": Python module exposing `build_timeline(fixed: bool) -> list[dict]` returning SceneTimelineFrame dicts
- "patch_rationale": brief explanation of initial risk or controller design
Return ONLY valid JSON. Never include markdown fences."""

PATCH_SYSTEM_PROMPT = """You are ProofForge 3D's counterexample-guided surgical patcher.
You are ONLY allowed to modify `system_impl_py`. NEVER modify `invariants_locked_py`.
Given the current `system_impl_py`, the locked `invariants_locked_py`, and the Z3 SAT counterexample trace,
return STRICT JSON with:
- "patched_system_impl_py": corrected Python code so `run_z3_check` proves UNSAT_PROVEN
- "patch_rationale": 1-2 sentence explanation of the root cause fix."""


def build_cogen_prompt(spec_text: str, inject_bug: bool = True) -> str:
    bug_clause = (
        "Include a realistic subtle edge-case bug in `system_impl_py` so Z3 initially finds a SAT counterexample."
        if inject_bug
        else "Generate a fully safe `system_impl_py` that immediately satisfies the invariant (UNSAT_PROVEN)."
    )
    return f"System Specification:\n{spec_text.strip()}\n\nRequirement:\n{bug_clause}"


def build_patch_prompt(
    system_impl_py: str,
    invariants_locked_py: str,
    counterexample: dict,
    violated_invariant: str | None,
) -> str:
    return (
        f"Locked Invariant (READ-ONLY):\n```python\n{invariants_locked_py}\n```\n\n"
        f"Current Buggy Implementation:\n```python\n{system_impl_py}\n```\n\n"
        f"Violated Invariant: {violated_invariant}\n"
        f"Z3 Counterexample Inputs: {counterexample}\n\n"
        "Patch `system_impl_py` surgically to eliminate the counterexample across the entire domain."
    )
