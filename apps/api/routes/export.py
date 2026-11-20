from fastapi import APIRouter

from ..models.schemas import VerificationResult

router = APIRouter()


@router.post("/api/forge/export")
async def forge_export(result: VerificationResult) -> dict:
    return {"exportUrl": f"/api/forge/export/{result.iteration}", "status": result.status}
