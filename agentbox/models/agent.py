"""Agent ORM model."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db.database import Base


# Lifecycle states from spec section 7.1.
AGENT_STATES = (
    "created",
    "starting",
    "running",
    "unhealthy",
    "restarting",
    "stopping",
    "stopped",
    "failed",
    "deleted",
)

RUNTIME_TYPES = ("hermes", "openclaw", "custom")


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(256), nullable=False)
    owner_id: Mapped[str] = mapped_column(
        String(32), ForeignKey("owners.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    runtime_type: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="created")
    container_name: Mapped[str] = mapped_column(String(256), nullable=False)
    image: Mapped[str] = mapped_column(String(256), nullable=False)
    data_dir: Mapped[str] = mapped_column(Text, nullable=False)
    cpu_limit: Mapped[str] = mapped_column(String(32), nullable=False, default="1")
    memory_limit: Mapped[str] = mapped_column(String(32), nullable=False, default="1g")
    disk_quota: Mapped[str | None] = mapped_column(String(32), nullable=True)
    auto_restart: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
