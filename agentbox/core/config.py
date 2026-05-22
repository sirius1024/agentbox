"""Runtime configuration loaded once per process."""
from __future__ import annotations

import os
from dataclasses import dataclass

from .paths import get_home


@dataclass(frozen=True)
class AppConfig:
    home: str
    admin_token: str | None
    bind_host: str
    bind_port: int

    @classmethod
    def load(cls) -> "AppConfig":
        return cls(
            home=str(get_home()),
            admin_token=os.environ.get("AGENTBOX_ADMIN_TOKEN"),
            bind_host=os.environ.get("AGENTBOX_HOST", "127.0.0.1"),
            bind_port=int(os.environ.get("AGENTBOX_PORT", "8765")),
        )


def get_config() -> AppConfig:
    return AppConfig.load()
