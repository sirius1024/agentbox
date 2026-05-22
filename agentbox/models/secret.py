"""Secret metadata ORM model.

Per spec section 12.3, secret VALUES must never appear in API
responses. This table only stores metadata. Encrypted material lives
in ``~/.agentbox/secrets/<scope>/<name>`` files written outside the
database (see :mod:`agentbox.services.secrets`).
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from ..db.database import Base


SECRET_SCOPES = ("platform", "agent")


class Secret(Base):
    __tablename__ = "secrets"
    __table_args__ = (UniqueConstraint("name", "scope", "agent_id", name="uq_secret_name_scope_agent"),)

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    scope: Mapped[str] = mapped_column(String(16), nullable=False)
    agent_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    exists: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
