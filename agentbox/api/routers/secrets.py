from __future__ import annotations

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from ...schemas.secret import SecretCreate, SecretOut
from ...services import secrets as svc
from ..deps import get_db, require_admin

router = APIRouter(prefix="/secrets", tags=["secrets"], dependencies=[Depends(require_admin)])


@router.post("", response_model=SecretOut, status_code=status.HTTP_201_CREATED)
def set_secret(payload: SecretCreate, db: Session = Depends(get_db)) -> SecretOut:
    """Create or replace a secret.

    The secret VALUE is write-only. The response contains only
    metadata. See spec section 12.3.
    """
    return SecretOut.model_validate(svc.set_secret(db, payload))


@router.get("", response_model=list[SecretOut])
def list_secrets(
    scope: str | None = Query(default=None),
    agent_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[SecretOut]:
    return [SecretOut.model_validate(s) for s in svc.list_secrets(db, scope=scope, agent_id=agent_id)]


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_secret(
    name: str,
    scope: str = Query(default="platform"),
    agent_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> None:
    svc.delete_secret(db, name=name, scope=scope, agent_id=agent_id)
