from __future__ import annotations

import typer

from ..schemas.owner import OwnerCreate, OwnerOut, OwnerUpdate
from ..services import owners as svc
from ._helpers import db_session, print_json, print_table

app = typer.Typer(help="Manage owners")


def _to_dict(o) -> dict:
    return OwnerOut.model_validate(o).model_dump(mode="json")


@app.command("create")
def create(
    name: str = typer.Argument(..., help="Unique slug, e.g. family-member-1"),
    display_name: str = typer.Option(..., "--display-name", "-d"),
    description: str | None = typer.Option(None, "--description"),
) -> None:
    """Create a new owner."""
    with db_session() as db:
        owner = svc.create_owner(
            db, OwnerCreate(name=name, display_name=display_name, description=description)
        )
        print_json(_to_dict(owner))


@app.command("list")
def list_cmd(
    output: str = typer.Option("table", "--output", "-o", help="table|json"),
) -> None:
    """List all owners."""
    with db_session() as db:
        owners = [_to_dict(o) for o in svc.list_owners(db)]
    if output == "json":
        print_json(owners)
    else:
        print_table(owners, ["id", "name", "display_name", "description"], title="Owners")


@app.command("show")
def show(owner_id: str) -> None:
    """Show an owner by id or name."""
    with db_session() as db:
        print_json(_to_dict(svc.get_owner(db, owner_id)))


@app.command("update")
def update(
    owner_id: str,
    display_name: str | None = typer.Option(None, "--display-name", "-d"),
    description: str | None = typer.Option(None, "--description"),
) -> None:
    """Update an owner's display name or description."""
    with db_session() as db:
        owner = svc.update_owner(
            db, owner_id, OwnerUpdate(display_name=display_name, description=description)
        )
        print_json(_to_dict(owner))


@app.command("delete")
def delete(
    owner_id: str,
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
) -> None:
    """Delete an owner that has no agents."""
    if not yes:
        typer.confirm(f"Delete owner '{owner_id}'?", abort=True)
    with db_session() as db:
        svc.delete_owner(db, owner_id)
    typer.echo(f"Deleted owner '{owner_id}'.")
