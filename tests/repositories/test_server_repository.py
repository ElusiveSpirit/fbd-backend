import pytest

from app.core.repositories import EntityDoesNotExist
from app.severs.models import Server
from app.severs.repositories import ServersRepository


def test_get_entity_does_not_exists_on_missing_slug(
    servers_repository: ServersRepository,
):
    missing_slug = "missing-slug"
    with pytest.raises(EntityDoesNotExist):
        servers_repository.get_server_by_slug(missing_slug)


def test_get_server_by_slug(servers_repository: ServersRepository):
    server_data = {
        "slug": "server-slug",
        "branch_name": "some-branch",
    }
    server = servers_repository.create_server(
        slug=server_data["slug"], branch_name=server_data["branch_name"],
    )
    assert server.slug == server_data["slug"]

    fetched_server = servers_repository.get_server_by_slug(server.slug)
    assert server.branch_name == fetched_server.branch_name


def test_get_empty_servers_list(servers_repository: ServersRepository):
    servers_list = servers_repository.get_servers_list()
    assert servers_list == []


def test_get_multiple_servers_in_list(servers_repository: ServersRepository):
    server_data = {
        "slug": "server-slug",
        "branch_name": "some-branch",
    }
    servers_repository.create_server(
        slug=server_data["slug"], branch_name=server_data["branch_name"],
    )
    servers_list = servers_repository.get_servers_list()
    assert len(servers_list) == 1
    assert servers_list[0].slug == server_data["slug"]


def test_delete_server(servers_repository: ServersRepository):
    server_data_list = [
        {"slug": "server-slug", "branch_name": "some-branch",},
        {"slug": "server-slug-2", "branch_name": "some-branch-2",},
    ]
    for server_data in server_data_list:
        servers_repository.create_server(
            slug=server_data["slug"], branch_name=server_data["branch_name"],
        )
    servers_list = servers_repository.get_servers_list()
    assert len(servers_list) == 2

    server_to_delete = Server(**server_data_list[0])
    servers_repository.delete_server(server_to_delete)

    servers_list = servers_repository.get_servers_list()
    assert len(servers_list) == 1
    assert servers_list[0].slug == server_data_list[1]["slug"]
