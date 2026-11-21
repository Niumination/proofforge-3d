from fastapi import APIRouter, HTTPException

from apps.api.models.schemas import ProofExportRequest, ProofExportResponse
from apps.api.security.credential_proxy import CredentialProxy, get_certificate

router = APIRouter()


@router.post("/api/forge/export", response_model=ProofExportResponse)
async def forge_export(payload: ProofExportRequest) -> ProofExportResponse:
    proxy = CredentialProxy()
    try:
        out = proxy.export_verified_proof(
            scenario_id=payload.scenario_id,
            result_dict=payload.result.model_dump(),
            impl_sha256=payload.impl_sha256,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ProofExportResponse(
        export_url=out["export_url"],
        certificate_id=out["certificate_id"],
        certificate_digest=out["certificate_digest"],
        proxy_audit=out["proxy_audit"],
    )


@router.get("/api/forge/certificate/{cert_id}")
async def fetch_certificate(cert_id: str) -> dict:
    cert = get_certificate(cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return cert
