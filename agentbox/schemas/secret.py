from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SecretCreate(BaseModel):
    """Create/update a secret.

    ``value`` is write-only: it never appears in any response.
    """

    name: str = Field(..., min_length=1, max_length=256)
    scope: Literal["platform", "agent"] = "platform"
    agent_id: str | None = None
    value: str = Field(..., min_length=1)


class SecretOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    scope: str
    agent_id: str | None
    exists: bool
    updated_at: datetime
