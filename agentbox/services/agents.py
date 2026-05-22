"""Agent service: pure business logic, no HTTP and no container runtime.

Container lifecycle (start/stop/logs/etc.) lives in the runtime driver
layer in later milestones. This module owns the database record and
the per-agent on-disk directory layout described in spec sections 5.3
and 8.2.
"""
from __future__ import annotations

from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.ids import new_id
from ..core.paths import agent_dir
from ..models.agent import Agent, RUNTIME_TYPES
from ..schemas.agent import AgentCreate, AgentUpdate
from .errors import ConflictError, NotFoundError, ValidationError
from .owners import get_owner


DEFAULT_IMAGES = {
    "hermes": "agentbox/hermes-runtime:dev",
    "openclaw": "agentbox/openclaw-runtime:dev",
    "custom": "agentbox/custom-runtime:dev",
}


def _container_name(runtime_type: str, name: str) -> str:
    return f"agentbox-{runtime_type}-{name}"


def _ensure_agent_dirs(agent_id: str, runtime_type: str) -> Path:
    """Create the per-agent directory tree.

    Layout per spec section 8.2 (Hermes example). For OpenClaw / custom
    we use the runtime name as the runtime-home subdirectory.
    """
    root = agent_dir(agent_id)
    runtime_home_name = "hermes" if runtime_type == "hermes" else runtime_type
    (root / runtime_home_name).mkdir(parents=True, exist_ok=True)
    (root / "workspace").mkdir(parents=True, exist_ok=True)
    (root / "backups").mkdir(parents=True, exist_ok=True)
    (root / "runtime").mkdir(parents=True, exist_ok=True)
    return root


def create_agent(db: Session, data: AgentCreate) -> Agent:
    if data.runtime_type not in RUNTIME_TYPES:
        raise ValidationError(f"Unknown runtime_type '{data.runtime_type}'")

    # Resolve owner (allows passing owner name as a convenience).
    owner = get_owner(db, data.owner_id)

    existing = db.scalar(select(Agent).where(Agent.name == data.name))
    if existing is not None:
        raise ConflictError(f"Agent with name '{data.name}' already exists")

    agent_id = new_id()
    image = data.image or DEFAULT_IMAGES.get(data.runtime_type, DEFAULT_IMAGES["custom"])
    root = _ensure_agent_dirs(agent_id, data.runtime_type)

    agent = Agent(
        id=agent_id,
        name=data.name,
        display_name=data.display_name or data.name,
        owner_id=owner.id,
        runtime_type=data.runtime_type,
        status="created",
        container_name=_container_name(data.runtime_type, data.name),
        image=image,
        data_dir=str(root),
        cpu_limit=data.cpu_limit,
        memory_limit=data.memory_limit,
        disk_quota=data.disk_quota,
        auto_restart=data.auto_restart,
        description=data.description,
    )
    db.add(agent)
    db.flush()
    return agent


def list_agents(
    db: Session,
    owner_id: str | None = None,
    runtime_type: str | None = None,
    status: str | None = None,
) -> list[Agent]:
    stmt = select(Agent).order_by(Agent.created_at)
    if owner_id:
        stmt = stmt.where(Agent.owner_id == owner_id)
    if runtime_type:
        stmt = stmt.where(Agent.runtime_type == runtime_type)
    if status:
        stmt = stmt.where(Agent.status == status)
    return list(db.scalars(stmt))


def get_agent(db: Session, agent_id: str) -> Agent:
    agent = db.get(Agent, agent_id)
    if agent is None:
        agent = db.scalar(select(Agent).where(Agent.name == agent_id))
    if agent is None:
        raise NotFoundError(f"Agent '{agent_id}' not found")
    return agent


def update_agent(db: Session, agent_id: str, data: AgentUpdate) -> Agent:
    agent = get_agent(db, agent_id)
    for field in (
        "display_name",
        "description",
        "cpu_limit",
        "memory_limit",
        "disk_quota",
        "auto_restart",
        "image",
    ):
        value = getattr(data, field)
        if value is not None:
            setattr(agent, field, value)
    db.flush()
    return agent


def delete_agent(db: Session, agent_id: str) -> None:
    agent = get_agent(db, agent_id)
    if agent.status in ("running", "starting", "restarting"):
        raise ConflictError(
            f"Agent '{agent.name}' is {agent.status}; stop it before delete"
        )
    db.delete(agent)
    db.flush()
