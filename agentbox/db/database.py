"""SQLAlchemy database setup."""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from ..core.paths import db_path, ensure_home


class Base(DeclarativeBase):
    pass


_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def _build_engine(url: str | None = None) -> Engine:
    if url is None:
        ensure_home()
        url = f"sqlite:///{db_path()}"
    engine = create_engine(
        url,
        future=True,
        connect_args={"check_same_thread": False} if url.startswith("sqlite") else {},
    )
    return engine


def init_db(url: str | None = None) -> Engine:
    """Initialize the database engine and create tables.

    Safe to call multiple times. Tests can pass a custom URL.
    """
    global _engine, _SessionLocal
    # Import models so their tables are registered on Base.metadata.
    from ..models import agent, owner, secret, settings  # noqa: F401

    _engine = _build_engine(url)
    _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)
    Base.metadata.create_all(_engine)
    return _engine


def get_engine() -> Engine:
    if _engine is None:
        init_db()
    assert _engine is not None
    return _engine


def get_sessionmaker() -> sessionmaker[Session]:
    if _SessionLocal is None:
        init_db()
    assert _SessionLocal is not None
    return _SessionLocal


@contextmanager
def session_scope() -> Iterator[Session]:
    """Context manager that yields a session and commits/rolls back."""
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


def reset_for_tests() -> None:
    """Discard cached engine so a new ``init_db`` call rebuilds it."""
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None
