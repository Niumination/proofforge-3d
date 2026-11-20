from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    proofforge_mode: str = "deterministic"
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    serve_static: bool = True
    web_dist_dir: str = "apps/web/dist"
    gemini_api_key: str = ""
    gemini_frontier_model: str = "gemini-4-argon"
    gemini_fast_model: str = "gemini-3.8-flash"
    gemini_managed_agent_id: str = "antigravity-preview-09-2026"
    managed_proxy_github_credential_ref: str = ""
    github_export_repo: str = "Niumination/proofforge-3d-proofs"


settings = Settings()
