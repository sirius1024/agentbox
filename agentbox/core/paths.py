"""Filesystem path helpers for AgentBox.

The default data directory is ``~/.agentbox`` but can be overridden via
the ``AGENTBOX_HOME`` environment variable. All internal code should go
through these helpers so tests can redirect the data directory.
"""
from __future__ import annotations

import os
from pathlib import Path

ENV_HOME = "AGENTBOX_HOME"
DEFAULT_HOME = "~/.agentbox"


def get_home() -> Path:
    """Return the AgentBox data directory.

    Resolution order:
    1. ``AGENTBOX_HOME`` environment variable, if set.
    2. ``~/.agentbox`` expanded against the current user's home.
    """
    raw = os.environ.get(ENV_HOME) or DEFAULT_HOME
    return Path(raw).expanduser().resolve()


def ensure_home() -> Path:
    """Ensure the AgentBox data directory exists and return it."""
    home = get_home()
    home.mkdir(parents=True, exist_ok=True)
    (home / "agents").mkdir(parents=True, exist_ok=True)
    (home / "secrets").mkdir(parents=True, exist_ok=True)
    (home / "runtime").mkdir(parents=True, exist_ok=True)
    return home


def db_path() -> Path:
    return get_home() / "agentbox.db"


def config_path() -> Path:
    return get_home() / "config.yaml"


def agent_dir(agent_id: str) -> Path:
    return get_home() / "agents" / agent_id
