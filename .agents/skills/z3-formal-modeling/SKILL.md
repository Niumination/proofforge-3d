---
name: z3-formal-modeling
description: Guidelines for fast, deterministic Z3 modeling (QF_LIA / quadratic without sqrt).
---
Use `z3.Real` or `z3.Int`, avoid `sqrt`/`sin`/`cos` in Z3 expressions, set timeout=8000ms.
