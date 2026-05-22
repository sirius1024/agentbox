from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient


def test_admin_token_required_when_configured(
    client: TestClient, monkeypatch, agentbox_home: Path
) -> None:
    monkeypatch.setenv("AGENTBOX_ADMIN_TOKEN", "secret-token")

    r = client.get("/owners")
    assert r.status_code == 401

    r = client.get("/owners", headers={"Authorization": "Bearer wrong"})
    assert r.status_code == 401

    r = client.get("/owners", headers={"Authorization": "Bearer secret-token"})
    assert r.status_code == 200

    # /health is unauthenticated.
    assert client.get("/health").status_code == 200
