from __future__ import annotations

import typer

from ..schemas.agent import AgentCreate, AgentOut, AgentUpdate
from ..services import agents as svc
from ._helpers import db_session, print_json, print_table

app = typer.Typer(help="Manage agents")


def _to_dict(a) -> dict:
    return AgentOut.model_validate(a).model_dump(mode="json")


@app.command("create")
def create(
    name: str = typer.Argument(..., help="Unique agent slug"),
    owner: str = typer.Option(..., "--owner", help="Owner id or name"),
    runtime: str = typer.Option("hermes", "--runtime", help="hermes|openclaw|custom"),
    display_name: str | None = typer.Option(None, "--display-name"),
    description: str | None = typer.Option(None, "--description"),
    cpu: str = typer.Option("1", "--cpu"),
    memory: str = typer.Option("1g", "--memory"),
    disk: str | None = typer.Option(None, "--disk"),
    image: str | None = typer.Option(None, "--image"),
    auto_restart: bool = typer.Option(True, "--auto-restart/--no-auto-restart"),
) -> None:
    """Create a new agent for an owner."""
    payload = AgentCreate(
        name=name,
        owner_id=owner,
        runtime_type=runtime,  # type: ignore[arg-type]
        display_name=display_name,
        description=description,
        cpu_limit=cpu,
        memory_limit=memory,
        disk_quota=disk,
        image=image,
        auto_restart=auto_restart,
    )
    with db_session() as db:
        agent = svc.create_agent(db, payload)
        print_json(_to_dict(agent))


@app.command("list")
def list_cmd(
    owner: str | None = typer.Option(None, "--owner"),
    runtime: str | None = typer.Option(None, "--runtime"),
    status: str | None = typer.Option(None, "--status"),
    output: str = typer.Option("table", "--output", "-o"),
) -> None:
    """List agents."""
    with db_session() as db:
        items = [
            _to_dict(a)
            for a in svc.list_agents(db, owner_id=owner, runtime_type=runtime, status=status)
        ]
    if output == "json":
        print_json(items)
    else:
        print_table(
            items,
            ["id", "name", "owner_id", "runtime_type", "status", "image"],
            title="Agents",
        )


@app.command("show")
def show(agent_id: str) -> None:
    """Show an agent by id or name."""
    with db_session() as db:
        print_json(_to_dict(svc.get_agent(db, agent_id)))


@app.command("update")
def update(
    agent_id: str,
    display_name: str | None = typer.Option(None, "--display-name"),
    description: str | None = typer.Option(None, "--description"),
    cpu: str | None = typer.Option(None, "--cpu"),
    memory: str | None = typer.Option(None, "--memory"),
    disk: str | None = typer.Option(None, "--disk"),
    image: str | None = typer.Option(None, "--image"),
    auto_restart: bool | None = typer.Option(None, "--auto-restart/--no-auto-restart"),
) -> None:
    """Update agent metadata or resource limits."""
    payload = AgentUpdate(
        display_name=display_name,
        description=description,
        cpu_limit=cpu,
        memory_limit=memory,
        disk_quota=disk,
        image=image,
        auto_restart=auto_restart,
    )
    with db_session() as db:
        print_json(_to_dict(svc.update_agent(db, agent_id, payload)))


@app.command("delete")
def delete(
    agent_id: str,
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Delete an agent record (container lifecycle handled separately)."""
    if not yes:
        typer.confirm(f"Delete agent '{agent_id}'?", abort=True)
    with db_session() as db:
        svc.delete_agent(db, agent_id)
    typer.echo(f"Deleted agent '{agent_id}'.")
