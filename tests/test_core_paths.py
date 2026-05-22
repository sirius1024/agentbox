from __future__ import annotations

from pathlib import Path

from agentbox.core.paths import agent_dir, db_path, ensure_home, get_home
from agentbox.db.database import get_sessionmaker, init_db


def test_home_uses_env_var(agentbox_home: Path) -> None:
    assert get_home() == agentbox_home.resolve()
    assert db_path().parent == agentbox_home.resolve()


def test_ensure_home_creates_subdirs(agentbox_home: Path) -> None:
    ensure_home()
    for sub in ("agents", "secrets", "runtime"):
        assert (agentbox_home / sub).is_dir()


def test_agent_dir(agentbox_home: Path) -> None:
    d = agent_dir("abc123")
    assert str(d).endswith("/agents/abc123")


def test_init_db_creates_tables(agentbox_home: Path) -> None:
    engine = init_db(f"sqlite:///{agentbox_home / 'agentbox.db'}")
    sm = get_sessionmaker()
    with sm() as session:
        # Smoke check: each table is queryable.
        from agentbox.models import Agent, Owner, Secret, Setting

        for model in (Owner, Agent, Secret, Setting):
            assert session.query(model).count() == 0
    engine.dispose()
