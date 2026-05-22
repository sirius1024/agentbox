"""Secret service.

Secret VALUES never appear in API responses or CLI output (spec 12.3).
For MVP we store values in mode-0600 files under
``<home>/secrets/<scope>/<name>`` (agent-scoped values go under
``<home>/secrets/agent/<agent_id>/<name>``). This is a SECURITY
LIMITATION (no encryption at rest); future versions should integrate a
keychain or encrypted store.
"""
from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.ids import new_id
from ..core.paths import ensure_home
from ..models.secret import Secret
from ..schemas.secret import SecretCreate
from .agents import get_agent
from .errors import NotFoundError, ValidationError


def _secret_path(scope: str, name: str, agent_id: str | None) -> Path:
    home = ensure_home()
    if scope == "platform":
        base = home / "secrets" / "platform"
    elif scope == "agent":
        if not agent_id:
            raise ValidationError("agent_id is required for scope='agent'")
        base = home / "secrets" / "agent" / agent_id
    else:
        raise ValidationError(f"Unknown secret scope '{scope}'")
    base.mkdir(parents=True, exist_ok=True)
    return base / name


def _write_value(path: Path, value: str) -> None:
    # Use os.open so we can set restrictive permissions atomically.
    flags = os.O_WRONLY | os.O_CREAT | os.O_TRUNC
    fd = os.open(str(path), flags, 0o600)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(value)
    finally:
        # fdopen closes fd; nothing else to do.
        pass
    try:
        os.chmod(path, 0o600)
    except OSError:  # pragma: no cover - best effort on non-POSIX
        pass


def set_secret(db: Session, data: SecretCreate) -> Secret:
    if data.scope == "agent":
        if not data.agent_id:
            raise ValidationError("agent_id is required for scope='agent'")
        # Validate agent exists.
        agent = get_agent(db, data.agent_id)
        agent_id = agent.id
    else:
        agent_id = None

    path = _secret_path(data.scope, data.name, agent_id)
    _write_value(path, data.value)

    existing = db.scalar(
        select(Secret).where(
            Secret.name == data.name,
            Secret.scope == data.scope,
            Secret.agent_id.is_(agent_id) if agent_id is None else Secret.agent_id == agent_id,
        )
    )
    if existing is None:
        existing = Secret(
            id=new_id(),
            name=data.name,
            scope=data.scope,
            agent_id=agent_id,
            exists=True,
        )
        db.add(existing)
    else:
        existing.exists = True
    db.flush()
    return existing


def list_secrets(
    db: Session, scope: str | None = None, agent_id: str | None = None
) -> list[Secret]:
    stmt = select(Secret).order_by(Secret.scope, Secret.name)
    if scope:
        stmt = stmt.where(Secret.scope == scope)
    if agent_id:
        stmt = stmt.where(Secret.agent_id == agent_id)
    return list(db.scalars(stmt))


def delete_secret(
    db: Session, name: str, scope: str = "platform", agent_id: str | None = None
) -> None:
    stmt = select(Secret).where(Secret.name == name, Secret.scope == scope)
    if scope == "agent":
        if not agent_id:
            raise ValidationError("agent_id is required for scope='agent'")
        stmt = stmt.where(Secret.agent_id == agent_id)
    secret = db.scalar(stmt)
    if secret is None:
        raise NotFoundError(f"Secret '{name}' not found in scope '{scope}'")

    path = _secret_path(scope, name, agent_id)
    try:
        path.unlink()
    except FileNotFoundError:
        pass
    db.delete(secret)
    db.flush()


def read_secret_value(
    name: str, scope: str = "platform", agent_id: str | None = None
) -> str | None:
    """Internal helper for the runtime layer to inject secrets into containers.

    This is NEVER exposed via API or CLI. Returns ``None`` if the
    secret file does not exist.
    """
    path = _secret_path(scope, name, agent_id)
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
