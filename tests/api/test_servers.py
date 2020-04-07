from fastapi.testclient import TestClient

from app.severs.models import Server, ServerStatus


def test_read_empty_all_servers(client: TestClient) -> None:
    response = client.get("/servers")
    assert response.status_code == 200
    assert response.json() == {"servers": [], "serversCount": 0}


def test_read_single_all_servers(client: TestClient, test_server_in_db: Server) -> None:
    response = client.get("/servers")
    assert response.status_code == 200
    data = response.json()
    assert data["serversCount"] == 1
    assert data["servers"][0]["slug"] == test_server_in_db.slug


def test_get_404_by_reading_nonexistent_server(client: TestClient) -> None:
    slug = "invalid-slug"
    response = client.get(f"/servers/{slug}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Server does not exists"}


def test_get_server_by_slug(client: TestClient, test_server_in_db: Server) -> None:
    response = client.get(f"/servers/{test_server_in_db.slug}")
    assert response.status_code == 200
    assert response.json() == {
        "server": {
            "slug": "server-slug",
            "branchName": "server-branch-name",
            "status": "stopped",
            "mrId": None,
            "mrIid": None,
            "mrStatus": None,
        }
    }


def test_update_server_by_slug(client: TestClient, test_server_in_db: Server) -> None:
    response = client.put(
        f"/servers/{test_server_in_db.slug}", json={"server": {"mrId": 1212}}
    )
    assert response.status_code == 200
    assert response.json() == {
        "server": {
            "slug": "server-slug",
            "branchName": "server-branch-name",
            "status": "stopped",
            "mrId": 1212,
            "mrIid": None,
            "mrStatus": None,
        }
    }


def test_delete_server_by_slug(client: TestClient, test_server_in_db: Server) -> None:
    response = client.delete(f"/servers/{test_server_in_db.slug}")
    assert response.status_code == 200

    response = client.get(f"/servers/{test_server_in_db.slug}")
    assert response.status_code == 404


def test_create_pending_server(client: TestClient, test_server: Server) -> None:
    test_server.status = ServerStatus.pending
    response = client.post(f"/servers", json={"server": test_server.dict()})
    assert response.status_code == 201
    assert response.json() == {
        "server": {
            "slug": "server-slug",
            "branchName": "server-branch-name",
            "status": "pending",
            "mrId": None,
            "mrIid": None,
            "mrStatus": None,
        }
    }


def test_create_server_that_exists(client: TestClient, test_server: Server) -> None:
    test_server.status = ServerStatus.pending
    response = client.post(f"/servers", json={"server": test_server.dict()})
    assert response.status_code == 201
    response = client.post(f"/servers", json={"server": test_server.dict()})
    assert response.status_code == 201


def test_update_server_status_by_slug(
    client: TestClient, test_server_in_db: Server
) -> None:
    response = client.put(
        f"/servers/{test_server_in_db.slug}",
        json={"server": {"status": ServerStatus.running}},
    )
    assert response.status_code == 200
    assert response.json()["server"]["status"] == "running"
