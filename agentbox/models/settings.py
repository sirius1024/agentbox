"""Platform settings ORM model.

Settings are stored as key/value rows so we can add new keys without
schema migrations during MVP.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from ..db.database import Base


# Known setting keys (see spec section 5.4).
KNOWN_KEYS = {
    "data_dir",
    "default_model_provider",
    "default_model_name",
    "runtime_driver",
    "podman_path",
    "admin_token_hash",
}


class Setting(Base):
    __tablename__ = "settings"

    key: Mapped[str] = mapped_column(String(128), primary_key=True)
    value: Mapped[str] = mapped_column(Text, nullable=False, default="")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
