from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

NAME_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$"

RuntimeType = Literal["hermes", "openclaw", "custom"]


class AgentCreate(BaseModel):
    name: str = Field(..., pattern=NAME_PATTERN)
    owner_id: str
    runtime_type: RuntimeType = "hermes"
    display_name: str | None = None
    description: str | None = None
    cpu_limit: str = "1"
    memory_limit: str = "1g"
    disk_quota: str | None = None
    auto_restart: bool = True
    image: str | None = None


class AgentUpdate(BaseModel):
    display_name: str | None = None
    description: str | None = None
    cpu_limit: str | None = None
    memory_limit: str | None = None
    disk_quota: str | None = None
    auto_restart: bool | None = None
    image: str | None = None


class AgentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    display_name: str
    owner_id: str
    runtime_type: str
    status: str
    container_name: str
    image: str
    data_dir: str
    cpu_limit: str
    memory_limit: str
    disk_quota: str | None
    auto_restart: bool
    description: str | None
    created_at: datetime
    updated_at: datetime
