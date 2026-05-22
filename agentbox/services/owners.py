"""Owner service: pure business logic, no HTTP."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.ids import new_id
from ..models.owner import Owner
from ..schemas.owner import OwnerCreate, OwnerUpdate
from .errors import ConflictError, NotFoundError


def create_owner(db: Session, data: OwnerCreate) -> Owner:
    existing = db.scalar(select(Owner).where(Owner.name == data.name))
    if existing is not None:
        raise ConflictError(f"Owner with name '{data.name}' already exists")
    owner = Owner(
        id=new_id(),
        name=data.name,
        display_name=data.display_name,
        description=data.description,
    )
    db.add(owner)
    db.flush()
    return owner


def list_owners(db: Session) -> list[Owner]:
    return list(db.scalars(select(Owner).order_by(Owner.created_at)))


def get_owner(db: Session, owner_id: str) -> Owner:
    owner = db.get(Owner, owner_id)
    if owner is None:
        # Allow lookup by name as a convenience.
        owner = db.scalar(select(Owner).where(Owner.name == owner_id))
    if owner is None:
        raise NotFoundError(f"Owner '{owner_id}' not found")
    return owner


def update_owner(db: Session, owner_id: str, data: OwnerUpdate) -> Owner:
    owner = get_owner(db, owner_id)
    if data.display_name is not None:
        owner.display_name = data.display_name
    if data.description is not None:
        owner.description = data.description
    db.flush()
    return owner


def delete_owner(db: Session, owner_id: str) -> None:
    from ..models.agent import Agent

    owner = get_owner(db, owner_id)
    agent_count = db.scalar(
        select(Agent.id).where(Agent.owner_id == owner.id).limit(1)
    )
    if agent_count is not None:
        raise ConflictError(
            f"Owner '{owner.name}' still has agents; delete agents first"
        )
    db.delete(owner)
    db.flush()
