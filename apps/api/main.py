from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes import forge, export

app = FastAPI(title="ProofForge 3D Orchestrator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health() -> dict:
    return {"status": "ok", "mode": settings.proofforge_mode}


app.include_router(forge.router)
app.include_router(export.router)
