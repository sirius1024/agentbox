from __future__ import annotations

from fastapi.testclient import TestClient


def test_owner_crud(client: TestClient) -> None:
    # Create
    r = client.post(
        "/owners",
        json={"name": "family-member-1", "display_name": "Family 1"},
    )
    assert r.status_code == 201, r.text
    owner = r.json()
    assert owner["name"] == "family-member-1"
    owner_id = owner["id"]

    # Duplicate
    r2 = client.post(
        "/owners",
        json={"name": "family-member-1", "display_name": "Dup"},
    )
    assert r2.status_code == 409

    # List
    r = client.get("/owners")
    assert r.status_code == 200
    assert len(r.json()) == 1

    # Get by id and by name
    assert client.get(f"/owners/{owner_id}").status_code == 200
    assert client.get("/owners/family-member-1").status_code == 200

    # Patch
    r = client.patch(f"/owners/{owner_id}", json={"display_name": "Renamed"})
    assert r.status_code == 200
    assert r.json()["display_name"] == "Renamed"

    # Delete
    r = client.delete(f"/owners/{owner_id}")
    assert r.status_code == 204
    assert client.get(f"/owners/{owner_id}").status_code == 404


def test_owner_with_agents_cannot_be_deleted(client: TestClient) -> None:
    owner = client.post(
        "/owners", json={"name": "primary", "display_name": "Primary"}
    ).json()
    client.post(
        "/agents",
        json={"name": "primary-hermes", "owner_id": owner["id"], "runtime_type": "hermes"},
    ).raise_for_status()
    r = client.delete(f"/owners/{owner['id']}")
    assert r.status_code == 409


def test_invalid_owner_name_rejected(client: TestClient) -> None:
    r = client.post("/owners", json={"name": "bad name with spaces", "display_name": "x"})
    assert r.status_code == 422
