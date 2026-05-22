from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...schemas.settings import SettingsOut, SettingsUpdate
from ...services import settings as svc
from ..deps import get_db, require_admin

router = APIRouter(prefix="/settings", tags=["settings"], dependencies=[Depends(require_admin)])


@router.get("", response_model=SettingsOut)
def read_settings(db: Session = Depends(get_db)) -> SettingsOut:
    return svc.get_settings(db)


@router.patch("", response_model=SettingsOut)
def update_settings(payload: SettingsUpdate, db: Session = Depends(get_db)) -> SettingsOut:
    return svc.update_settings(db, payload)
