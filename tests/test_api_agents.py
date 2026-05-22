from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient


def _make_owner(client: TestClient) -> str:
    r = client.post("/owners", json={"name": "primary", "display_name": "Primary"})
    assert r.status_code == 201
    return r.json()["id"]


def test_agent_crud_and_dir_layout(client: TestClient, agentbox_home: Path) -> None:
    owner_id = _make_owner(client)

    r = client.post(
        "/agents",
        json={
            "name": "primary-hermes",
            "owner_id": owner_id,
            "runtime_type": "hermes",
            "cpu_limit": "0.5",
            "memory_limit": "512m",
        },
    )
    assert r.status_code == 201, r.text
    agent = r.json()
    assert agent["status"] == "created"
    assert agent["runtime_type"] == "hermes"
    assert agent["container_name"] == "agentbox-hermes-primary-hermes"
    assert agent["image"].startswith("agentbox/hermes-runtime")
    assert agent["cpu_limit"] == "0.5"
    assert agent["data_dir"].startswith(str(agentbox_home))

    # Directories were created per spec section 8.2.
    agent_root = Path(agent["data_dir"])
    assert (agent_root / "hermes").is_dir()
    assert (agent_root / "workspace").is_dir()
    assert (agent_root / "backups").is_dir()
    assert (agent_root / "runtime").is_dir()

    # Duplicate name rejected
    r2 = client.post(
        "/agents",
        json={"name": "primary-hermes", "owner_id": owner_id, "runtime_type": "hermes"},
    )
    assert r2.status_code == 409

    # List + filter by owner
    r = client.get("/agents", params={"owner_id": owner_id})
    assert r.status_code == 200
    assert len(r.json()) == 1

    # Patch
    r = client.patch(f"/agents/{agent['id']}", json={"memory_limit": "2g"})
    assert r.status_code == 200
    assert r.json()["memory_limit"] == "2g"

    # Delete
    r = client.delete(f"/agents/{agent['id']}")
    assert r.status_code == 204


def test_agent_requires_known_owner(client: TestClient) -> None:
    r = client.post(
        "/agents",
        json={"name": "ghost", "owner_id": "does-not-exist", "runtime_type": "hermes"},
    )
    assert r.status_code == 404


def test_openclaw_runtime_supported(client: TestClient) -> None:
    owner_id = _make_owner(client)
    r = client.post(
        "/agents",
        json={"name": "primary-claw", "owner_id": owner_id, "runtime_type": "openclaw"},
    )
    assert r.status_code == 201
    assert r.json()["image"].startswith("agentbox/openclaw-runtime")
