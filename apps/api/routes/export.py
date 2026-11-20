from fastapi import APIRouter

from ..models.schemas import VerificationResult

router = APIRouter(prefix="/api/forge")


@router.post("/export")
async def forge_export(result: VerificationResult) -> dict:
    # Phase 1: export via Credential Proxy (Phase 3); Phase 1 cukup mengembalikan metadata
    return {"exportUrl": f"/api/forge/export/{result.iteration}", "status": result.status}
