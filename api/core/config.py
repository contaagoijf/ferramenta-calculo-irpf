from __future__ import annotations

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    # Supabase
    supabase_url: str = Field(..., env="SUPABASE_URL")
    supabase_key: str = Field(..., env="SUPABASE_KEY")

    # FastAPI
    api_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @validator("supabase_url")
    def ensure_trailing_slash(cls, v: str) -> str:
        return v.rstrip("/")


settings = Settings()