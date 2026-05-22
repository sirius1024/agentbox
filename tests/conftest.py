"""Shared pytest fixtures.

Every test gets a fresh ``AGENTBOX_HOME`` under a temp dir and a fresh
in-memory SQLite database so tests cannot interfere with the user's
real ``~/.agentbox`` directory.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from agentbox.api.app import create_app
from agentbox.db import database


@pytest.fixture()
def agentbox_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "agentbox-home"
    home.mkdir()
    monkeypatch.setenv("AGENTBOX_HOME", str(home))
    monkeypatch.delenv("AGENTBOX_ADMIN_TOKEN", raising=False)
    database.reset_for_tests()
    database.init_db(f"sqlite:///{home / 'agentbox.db'}")
    yield home
    database.reset_for_tests()


@pytest.fixture()
def db(agentbox_home: Path) -> Iterator[Session]:
    sm = database.get_sessionmaker()
    session = sm()
    try:
        yield session
        session.commit()
    finally:
        session.close()


@pytest.fixture()
def client(agentbox_home: Path) -> Iterator[TestClient]:
    app = create_app()
    with TestClient(app) as c:
        yield c
