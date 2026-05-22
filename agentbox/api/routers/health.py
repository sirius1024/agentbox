from __future__ import annotations

from fastapi import APIRouter

from ... import __version__

router = APIRouter(tags=["system"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": __version__}
