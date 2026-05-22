from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


NAME_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,63}$"


class OwnerCreate(BaseModel):
    name: str = Field(..., pattern=NAME_PATTERN, description="Short unique slug")
    display_name: str = Field(..., min_length=1, max_length=256)
    description: str | None = None


class OwnerUpdate(BaseModel):
    display_name: str | None = Field(default=None, min_length=1, max_length=256)
    description: str | None = None


class OwnerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    display_name: str
    description: str | None
    created_at: datetime
    updated_at: datetime
