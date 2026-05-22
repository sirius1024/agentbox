from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient


def test_settings_defaults_and_update(client: TestClient, agentbox_home: Path) -> None:
    r = client.get("/settings")
    assert r.status_code == 200
    body = r.json()
    assert body["data_dir"] == str(agentbox_home.resolve())
    assert body["runtime_driver"] == "podman"
    assert body["admin_token_configured"] is False

    r = client.patch(
        "/settings",
        json={"default_model_provider": "openrouter", "default_model_name": "anthropic/claude-sonnet-4"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["default_model_provider"] == "openrouter"
    assert body["default_model_name"] == "anthropic/claude-sonnet-4"


def test_secret_metadata_never_leaks_value(client: TestClient, agentbox_home: Path) -> None:
    secret_value = "sk-super-secret-do-not-leak-123"
    r = client.post(
        "/secrets",
        json={"name": "OPENROUTER_API_KEY", "scope": "platform", "value": secret_value},
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["name"] == "OPENROUTER_API_KEY"
    assert body["scope"] == "platform"
    assert body["exists"] is True
    # Critical: value must never appear in the response payload.
    assert secret_value not in r.text
    assert "value" not in body

    r = client.get("/secrets")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert secret_value not in r.text

    # On-disk secret file must be mode 0600.
    secret_path = agentbox_home / "secrets" / "platform" / "OPENROUTER_API_KEY"
    assert secret_path.is_file()
    mode = secret_path.stat().st_mode & 0o777
    assert mode == 0o600
    assert secret_path.read_text() == secret_value

    # Delete
    r = client.delete("/secrets/OPENROUTER_API_KEY", params={"scope": "platform"})
    assert r.status_code == 204
    assert not secret_path.exists()


def test_agent_scoped_secret_requires_agent_id(client: TestClient) -> None:
    r = client.post(
        "/secrets",
        json={"name": "TELEGRAM_TOKEN", "scope": "agent", "value": "x"},
    )
    assert r.status_code == 400
