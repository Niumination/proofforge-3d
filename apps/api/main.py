from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from apps.api.config import settings
from apps.api.routes import export, forge

app = FastAPI(title="ProofForge 3D Orchestrator", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _dist_dir() -> Path:
    return Path(settings.web_dist_dir).resolve()


@app.get("/api/health")
async def health() -> dict:
    dist_index = _dist_dir() / "index.html"
    return {
        "status": "ok",
        "mode": settings.proofforge_mode,
        "static_ui_ready": settings.serve_static and dist_index.is_file(),
    }


app.include_router(forge.router)
app.include_router(export.router)


def configure_static_ui(target_app: FastAPI, dist_path: Path | None = None) -> bool:
    dist = (dist_path or _dist_dir()).resolve()
    index_file = dist / "index.html"
    if not settings.serve_static or not index_file.is_file():
        return False

    assets_dir = dist / "assets"
    if assets_dir.is_dir():
        target_app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @target_app.get("/{full_path:path}", include_in_schema=False)
    async def spa_fallback(full_path: str) -> FileResponse:
        if full_path == "api" or full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        candidate = (dist / full_path).resolve()
        if full_path and dist in candidate.parents and candidate.is_file():
            return FileResponse(candidate)
        return FileResponse(index_file)

    return True


configure_static_ui(app)
