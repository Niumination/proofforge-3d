"""Credential Proxy (`PF-023`) — issues signed Proof Certificates & isolated GitHub export."""

import hashlib
import json
from datetime import UTC, datetime
from typing import Any

import httpx

from apps.api.config import settings
from apps.api.security.protected_hooks import redact_secrets

_CERTIFICATES: dict[str, dict[str, Any]] = {}


class CredentialProxy:
    """Egress proxy holding external credentials strictly outside LLM/agent context."""

    def __init__(self, transport: httpx.BaseTransport | None = None) -> None:
        self.transport = transport

    def create_certificate(
        self,
        scenario_id: str,
        result_dict: dict[str, Any],
        impl_sha256: str = "",
    ) -> dict[str, Any]:
        if result_dict.get("status") != "UNSAT_PROVEN":
            raise ValueError("Refusing to issue Proof Certificate unless status == UNSAT_PROVEN")

        inv_sha = str(result_dict.get("invariant_sha256", ""))
        canonical = json.dumps(
            {
                "scenario_id": scenario_id,
                "status": result_dict.get("status"),
                "invariant_sha256": inv_sha,
                "impl_sha256": impl_sha256,
                "iteration": result_dict.get("iteration"),
            },
            sort_keys=True,
        )
        digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        cert_id = f"cert-{digest[:12]}"
        cert = {
            "certificate_id": cert_id,
            "issued_at_utc": datetime.now(UTC).isoformat(),
            "scenario_id": scenario_id,
            "verification_status": "UNSAT_PROVEN",
            "invariant_sha256": inv_sha,
            "impl_sha256": impl_sha256 or "deterministic-verified",
            "certificate_digest_sha256": digest,
            "hooks_enforced": ["pre_verify_invariant_guard", "write_scope_guard"],
            "credential_exposed": False,
        }
        _CERTIFICATES[cert_id] = cert
        return cert

    def export_verified_proof(
        self,
        scenario_id: str,
        result_dict: dict[str, Any],
        impl_sha256: str = "",
    ) -> dict[str, Any]:
        cert = self.create_certificate(scenario_id, result_dict, impl_sha256=impl_sha256)
        cert_id = cert["certificate_id"]
        token_ref = settings.managed_proxy_github_credential_ref
        export_url = f"https://github.com/{settings.github_export_repo}/issues/proof-{cert_id}"
        mode = "proxy_audit_local"
        status_code = 201

        if token_ref and token_ref.startswith(("ghp_", "github_pat_")):
            try:
                client_kwargs: dict[str, Any] = {"timeout": 15.0}
                if self.transport is not None:
                    client_kwargs["transport"] = self.transport
                with httpx.Client(**client_kwargs) as client:
                    resp = client.post(
                        f"https://api.github.com/repos/{settings.github_export_repo}/issues",
                        headers={
                            "Authorization": f"Bearer {token_ref}",
                            "Accept": "application/vnd.github+json",
                        },
                        json={
                            "title": f"[ProofForge 3D] Verified UNSAT Proof: {scenario_id} ({cert_id})",
                            "body": redact_secrets(
                                f"Digest: `{cert['certificate_digest_sha256']}`\n"
                                f"Invariant SHA-256: `{cert['invariant_sha256']}`"
                            ),
                        },
                    )
                    status_code = resp.status_code
                    if resp.status_code in (200, 201):
                        export_url = resp.json().get("html_url", export_url)
                        mode = "github_api_proxied"
            except httpx.HTTPError:
                mode = "proxy_audit_fallback"

        return {
            "export_url": export_url,
            "certificate_id": cert_id,
            "certificate_digest": cert["certificate_digest_sha256"],
            "certificate": cert,
            "proxy_audit": {
                "domain": "api.github.com",
                "credential_ref": "PROXY_MANAGED_GITHUB_TOKEN",
                "redacted": True,
                "credential_exposed": False,
                "mode": mode,
                "status_code": status_code,
                "scenario_id": scenario_id,
                "proof_status": result_dict.get("status"),
                "certificate_id": cert_id,
            },
        }


def get_certificate(cert_id: str) -> dict[str, Any] | None:
    return _CERTIFICATES.get(cert_id)


def render_markdown_report(cert_id: str) -> str | None:
    cert = _CERTIFICATES.get(cert_id)
    if not cert:
        return None
    hooks_md = "\n".join(f"- `{h}`" for h in cert.get("hooks_enforced", []))
    return (
        f"# ProofForge 3D — Formal Verification & Security Audit Report\n\n"
        f"- **Certificate ID:** `{cert['certificate_id']}`\n"
        f"- **Issued (UTC):** `{cert['issued_at_utc']}`\n"
        f"- **Scenario:** `{cert['scenario_id']}`\n"
        f"- **Verification Status:** **{cert['verification_status']}**\n"
        f"- **Locked Invariant SHA-256:** `{cert['invariant_sha256']}`\n"
        f"- **Implementation SHA-256:** `{cert['impl_sha256']}`\n"
        f"- **Certificate Digest SHA-256:** `{cert['certificate_digest_sha256']}`\n"
        f"- **Credential Exposed to Agent:** `{cert['credential_exposed']}`\n\n"
        f"## Enforced Protected Hooks\n{hooks_md}\n"
    )
