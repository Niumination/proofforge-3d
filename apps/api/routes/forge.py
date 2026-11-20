from fastapi import APIRouter

from ..models.schemas import ForgeRunRequest

router = APIRouter(prefix="/api/forge")


@router.post("/run")
async def forge_run(request: ForgeRunRequest) -> dict:
    # Phase 1: deterministic engine — akan diisi di PF-007/PF-008
    return {"runId": "run-deterministic-001"}
