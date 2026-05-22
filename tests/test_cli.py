from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from agentbox.cli.main import app

runner = CliRunner()


def test_cli_init_creates_home(agentbox_home: Path) -> None:
    result = runner.invoke(app, ["init"])
    assert result.exit_code == 0, result.output
    assert (agentbox_home / "agentbox.db").exists()
    assert (agentbox_home / "agents").is_dir()


def test_cli_owner_and_agent_flow(agentbox_home: Path) -> None:
    r = runner.invoke(app, ["init"])
    assert r.exit_code == 0

    r = runner.invoke(
        app, ["owner", "create", "family-1", "--display-name", "Family 1"]
    )
    assert r.exit_code == 0, r.output
    assert "family-1" in r.output

    r = runner.invoke(app, ["owner", "list", "--output", "json"])
    assert r.exit_code == 0
    assert "family-1" in r.output

    r = runner.invoke(
        app,
        [
            "agent", "create", "family-hermes",
            "--owner", "family-1",
            "--runtime", "hermes",
        ],
    )
    assert r.exit_code == 0, r.output
    assert "family-hermes" in r.output

    r = runner.invoke(app, ["agent", "list", "--output", "json"])
    assert r.exit_code == 0
    assert "family-hermes" in r.output


def test_cli_config_and_secret_no_value_leak(agentbox_home: Path) -> None:
    assert runner.invoke(app, ["init"]).exit_code == 0

    r = runner.invoke(app, ["config", "set", "model.provider", "openrouter"])
    assert r.exit_code == 0
    r = runner.invoke(app, ["config", "get", "model.provider"])
    assert r.exit_code == 0
    assert r.output.strip() == "openrouter"

    # set secret via --value option, then verify list output has no value
    secret_value = "sk-do-not-leak-XYZ"
    r = runner.invoke(
        app,
        ["secret", "set", "OPENROUTER_API_KEY", "--scope", "platform", "--value", secret_value],
    )
    assert r.exit_code == 0, r.output
    assert secret_value not in r.output

    r = runner.invoke(app, ["secret", "list", "--output", "json"])
    assert r.exit_code == 0
    assert secret_value not in r.output
    assert "OPENROUTER_API_KEY" in r.output
