"""Platform settings service."""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..core.paths import get_home
from ..models.settings import Setting
from ..schemas.settings import SettingsOut, SettingsUpdate


DEFAULTS: dict[str, str] = {
    "runtime_driver": "podman",
    "podman_path": "podman",
}


def _get_value(db: Session, key: str) -> str | None:
    row = db.get(Setting, key)
    return row.value if row else None


def _set_value(db: Session, key: str, value: str | None) -> None:
    row = db.get(Setting, key)
    if value is None:
        if row is not None:
            db.delete(row)
        return
    if row is None:
        db.add(Setting(key=key, value=value))
    else:
        row.value = value


def get_settings(db: Session) -> SettingsOut:
    return SettingsOut(
        data_dir=str(get_home()),
        default_model_provider=_get_value(db, "default_model_provider"),
        default_model_name=_get_value(db, "default_model_name"),
        runtime_driver=_get_value(db, "runtime_driver") or DEFAULTS["runtime_driver"],
        podman_path=_get_value(db, "podman_path") or DEFAULTS["podman_path"],
        admin_token_configured=_get_value(db, "admin_token_hash") is not None,
    )


def update_settings(db: Session, data: SettingsUpdate) -> SettingsOut:
    payload = data.model_dump(exclude_unset=True)
    for key, value in payload.items():
        _set_value(db, key, value)
    db.flush()
    return get_settings(db)


def get_setting_raw(db: Session, key: str) -> str | None:
    """Return a raw setting value (used by CLI ``config get``)."""
    value = _get_value(db, key)
    if value is None and key in DEFAULTS:
        return DEFAULTS[key]
    if value is None and key == "data_dir":
        return str(get_home())
    return value


def set_setting_raw(db: Session, key: str, value: str | None) -> None:
    _set_value(db, key, value)
    db.flush()


def list_settings(db: Session) -> dict[str, str]:
    rows = db.scalars(select(Setting))
    result = dict(DEFAULTS)
    result["data_dir"] = str(get_home())
    for row in rows:
        if row.key == "admin_token_hash":
            continue  # never expose the hash via config listings
        result[row.key] = row.value
    return result
