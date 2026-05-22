from __future__ import annotations

from pydantic import BaseModel, Field


class SettingsOut(BaseModel):
    data_dir: str
    default_model_provider: str | None = None
    default_model_name: str | None = None
    runtime_driver: str = "podman"
    podman_path: str | None = None
    admin_token_configured: bool = False


class SettingsUpdate(BaseModel):
    default_model_provider: str | None = Field(default=None, max_length=128)
    default_model_name: str | None = Field(default=None, max_length=256)
    runtime_driver: str | None = Field(default=None, max_length=64)
    podman_path: str | None = Field(default=None, max_length=512)
