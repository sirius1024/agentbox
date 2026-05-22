from __future__ import annotations

import typer

from ..services import settings as svc
from ._helpers import db_session, print_json, print_table

app = typer.Typer(help="Get or set platform configuration")


_ALLOWED_KEYS = {
    "model.provider": "default_model_provider",
    "model.default": "default_model_name",
    "runtime.driver": "runtime_driver",
    "runtime.podman_path": "podman_path",
}


def _normalize(key: str) -> str:
    if key in _ALLOWED_KEYS:
        return _ALLOWED_KEYS[key]
    if key in _ALLOWED_KEYS.values() or key in ("data_dir",):
        return key
    raise typer.BadParameter(
        f"Unknown config key '{key}'. Allowed: {sorted(_ALLOWED_KEYS) + ['data_dir']}"
    )


@app.command("get")
def get(key: str) -> None:
    """Get a config value (never returns secrets)."""
    normalized = _normalize(key)
    with db_session() as db:
        value = svc.get_setting_raw(db, normalized)
    typer.echo(value if value is not None else "")


@app.command("set")
def set_cmd(key: str, value: str) -> None:
    """Set a config value."""
    normalized = _normalize(key)
    with db_session() as db:
        svc.set_setting_raw(db, normalized, value)
    typer.echo(f"Set {key} = {value}")


@app.command("list")
def list_cmd(output: str = typer.Option("table", "--output", "-o")) -> None:
    """List all platform settings (no secret values)."""
    with db_session() as db:
        data = svc.list_settings(db)
    if output == "json":
        print_json(data)
    else:
        print_table(
            [{"key": k, "value": v} for k, v in sorted(data.items())],
            ["key", "value"],
            title="Settings",
        )
