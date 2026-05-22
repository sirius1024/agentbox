"""Short identifier generation for AgentBox entities."""
from __future__ import annotations

import secrets


def new_id(prefix: str = "") -> str:
    """Return a short URL-safe identifier.

    The id is 12 hex chars (~48 bits). Collisions inside a single
    deployment are vanishingly unlikely for personal/family scale.
    """
    raw = secrets.token_hex(6)
    return f"{prefix}{raw}" if prefix else raw
