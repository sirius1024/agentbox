"""FastAPI dependencies."""
from __future__ import annotations

import hashlib
from typing import Iterator

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from ..core.config import get_config
from ..db.database import get_sessionmaker
from ..services import settings as settings_service


def get_db() -> Iterator[Session]:
    sm = get_sessionmaker()
    session = sm()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def require_admin(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> None:
    """Validate bearer token against configured admin token.

    Resolution order:
    1. ``AGENTBOX_ADMIN_TOKEN`` env var (plaintext compare).
    2. ``admin_token_hash`` setting (sha256 compare).
    3. If neither is configured, auth is OPEN (single-user dev mode).
       This matches spec section 11 where the token is initialized by
       ``agentbox init``; if it has not been set yet, the API is
       reachable on localhost only (see ``AGENTBOX_HOST``).
    """
    cfg = get_config()
    env_token = cfg.admin_token
    stored_hash = settings_service.get_setting_raw(db, "admin_token_hash")

    if not env_token and not stored_hash:
        return  # dev mode: no auth configured yet

    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    presented = authorization.split(" ", 1)[1].strip()

    if env_token and presented == env_token:
        return
    if stored_hash and _hash_token(presented) == stored_hash:
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid admin token",
        headers={"WWW-Authenticate": "Bearer"},
    )
