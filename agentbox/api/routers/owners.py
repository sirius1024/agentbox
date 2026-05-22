from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ...schemas.owner import OwnerCreate, OwnerOut, OwnerUpdate
from ...services import owners as svc
from ..deps import get_db, require_admin

router = APIRouter(prefix="/owners", tags=["owners"], dependencies=[Depends(require_admin)])


@router.post("", response_model=OwnerOut, status_code=status.HTTP_201_CREATED)
def create_owner(payload: OwnerCreate, db: Session = Depends(get_db)) -> OwnerOut:
    return OwnerOut.model_validate(svc.create_owner(db, payload))


@router.get("", response_model=list[OwnerOut])
def list_owners(db: Session = Depends(get_db)) -> list[OwnerOut]:
    return [OwnerOut.model_validate(o) for o in svc.list_owners(db)]


@router.get("/{owner_id}", response_model=OwnerOut)
def get_owner(owner_id: str, db: Session = Depends(get_db)) -> OwnerOut:
    return OwnerOut.model_validate(svc.get_owner(db, owner_id))


@router.patch("/{owner_id}", response_model=OwnerOut)
def update_owner(
    owner_id: str, payload: OwnerUpdate, db: Session = Depends(get_db)
) -> OwnerOut:
    return OwnerOut.model_validate(svc.update_owner(db, owner_id, payload))


@router.delete("/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_owner(owner_id: str, db: Session = Depends(get_db)) -> None:
    svc.delete_owner(db, owner_id)
