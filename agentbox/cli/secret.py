from __future__ import annotations

import sys

import typer

from ..schemas.secret import SecretCreate, SecretOut
from ..services import secrets as svc
from ._helpers import db_session, print_json, print_table

app = typer.Typer(help="Manage platform and agent secrets")


def _to_dict(s) -> dict:
    return SecretOut.model_validate(s).model_dump(mode="json")


@app.command("set")
def set_cmd(
    name: str = typer.Argument(..., help="Secret name, e.g. OPENROUTER_API_KEY"),
    scope: str = typer.Option("platform", "--scope", help="platform|agent"),
    agent: str | None = typer.Option(None, "--agent", help="Agent id (required for scope=agent)"),
    value: str | None = typer.Option(
        None,
        "--value",
        help="Secret value. If omitted, read from stdin. Never echoed.",
    ),
) -> None:
    """Create or update a secret. Value is write-only and never displayed."""
    if value is None:
        if sys.stdin.isatty():
            value = typer.prompt(f"Value for {name}", hide_input=True, confirmation_prompt=True)
        else:
            value = sys.stdin.read().rstrip("\n")
    if not value:
        raise typer.BadParameter("Secret value must not be empty")

    with db_session() as db:
        secret = svc.set_secret(
            db,
            SecretCreate(name=name, scope=scope, agent_id=agent, value=value),  # type: ignore[arg-type]
        )
        # Output metadata only.
        print_json(_to_dict(secret))


@app.command("list")
def list_cmd(
    scope: str | None = typer.Option(None, "--scope"),
    agent: str | None = typer.Option(None, "--agent"),
    output: str = typer.Option("table", "--output", "-o"),
) -> None:
    """List secret metadata (never values)."""
    with db_session() as db:
        items = [_to_dict(s) for s in svc.list_secrets(db, scope=scope, agent_id=agent)]
    if output == "json":
        print_json(items)
    else:
        print_table(items, ["name", "scope", "agent_id", "exists", "updated_at"], title="Secrets")


@app.command("delete")
def delete(
    name: str,
    scope: str = typer.Option("platform", "--scope"),
    agent: str | None = typer.Option(None, "--agent"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Delete a secret."""
    if not yes:
        typer.confirm(f"Delete secret '{name}' ({scope})?", abort=True)
    with db_session() as db:
        svc.delete_secret(db, name=name, scope=scope, agent_id=agent)
    typer.echo(f"Deleted secret '{name}'.")
