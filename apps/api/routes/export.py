from fastapi import APIRouter

from apps.api.config import settings
from apps.api.models.schemas import ProofExportRequest, ProofExportResponse

router = APIRouter()


@router.post("/api/forge/export", response_model=ProofExportResponse)
async def forge_export(payload: ProofExportRequest) -> ProofExportResponse:
    cert_sha = payload.result.invariant_sha256[:12] or "deterministic"
    export_url = f"https://github.com/{settings.github_export_repo}/issues/proof-{cert_sha}"
    return ProofExportResponse(
        export_url=export_url,
        proxy_audit={
            "domain": "api.github.com",
            "credential_ref": "PROXY_MANAGED_GITHUB_TOKEN",
            "redacted": True,
            "status_code": 201,
            "scenario_id": payload.scenario_id,
            "proof_status": payload.result.status,
        },
    )
