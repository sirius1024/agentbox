"""Shared helpers for CLI commands."""
from __future__ import annotations

import json
from contextlib import contextmanager
from typing import Any, Iterator

import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from ..db.database import get_sessionmaker, init_db

console = Console()


@contextmanager
def db_session() -> Iterator[Session]:
    init_db()
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


def print_json(data: Any) -> None:
    typer.echo(json.dumps(data, indent=2, default=str, ensure_ascii=False))


def print_table(rows: list[dict[str, Any]], columns: list[str], title: str | None = None) -> None:
    table = Table(title=title)
    for col in columns:
        table.add_column(col)
    for row in rows:
        table.add_row(*[str(row.get(c, "")) for c in columns])
    console.print(table)
