#!/usr/bin/env python3
"""Hackathon-morning API preflight (`PF-019`) for Gemini 4 Argon & Managed Agents."""

import sys

import httpx
import z3

from apps.api.config import settings


def main() -> int:
    print(f"[PREFLIGHT] z3-solver version: {z3.get_version_string()}")
    print(f"[PREFLIGHT] mode={settings.proofforge_mode} frontier={settings.gemini_frontier_model}")
    print(f"[PREFLIGHT] managed_agent={settings.gemini_managed_agent_id}")

    if not settings.gemini_api_key:
        print("[PREFLIGHT] GEMINI_API_KEY not set — deterministic fallback ready.")
        return 0

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_frontier_model}"
    try:
        with httpx.Client(timeout=15.0) as client:
            res = client.get(url, headers={"x-goog-api-key": settings.gemini_api_key})
        print(f"[PREFLIGHT] Gemini model check HTTP {res.status_code}")
        return 0 if res.status_code == 200 else 1
    except httpx.HTTPError as exc:
        print(f"[PREFLIGHT] Network check failed ({exc}); offline deterministic fallback ready.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
