"""Top-level ``agentbox`` CLI entrypoint."""
from __future__ import annotations

import typer

from ..core.paths import db_path, ensure_home, get_home
from ..db.database import init_db
from . import agent as agent_cli
from . import config_cmd
from . import owner as owner_cli
from . import secret as secret_cli

app = typer.Typer(help="AgentBox: lightweight multi-agent management platform", no_args_is_help=True)

app.add_typer(owner_cli.app, name="owner")
app.add_typer(agent_cli.app, name="agent")
app.add_typer(config_cmd.app, name="config")
app.add_typer(secret_cli.app, name="secret")


@app.command()
def init() -> None:
    """Initialize the AgentBox data directory and database."""
    home = ensure_home()
    init_db()
    typer.echo(f"Initialized AgentBox at {home}")
    typer.echo(f"Database: {db_path()}")


@app.command()
def status() -> None:
    """Show basic AgentBox status."""
    typer.echo(f"AgentBox home: {get_home()}")
    typer.echo(f"Database: {db_path()}")


@app.command()
def server(
    host: str = typer.Option("127.0.0.1", "--host", help="Bind host (default localhost only)"),
    port: int = typer.Option(8765, "--port"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload (dev only)"),
) -> None:
    """Run the AgentBox HTTP API server."""
    import uvicorn

    ensure_home()
    init_db()
    uvicorn.run("agentbox.api.app:app", host=host, port=port, reload=reload)


if __name__ == "__main__":  # pragma: no cover
    app()
