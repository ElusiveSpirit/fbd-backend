from pytest_mock import MockFixture, pytest

from app.core.repositories import EntityDoesNotExist
from app.severs.models import Server, ServerStatus
from app.severs.repositories import ServerIsBusy, ServersRepository
from app.severs.services import clean_server


def test_clean_server(
    mocker: MockFixture,
    servers_repository: ServersRepository,
    test_server_in_db: Server,
) -> None:
    mocker.patch("app.severs.services.run_clean_playbook")
    assert clean_server(servers_repository, test_server_in_db.slug) is None
    with pytest.raises(EntityDoesNotExist):
        servers_repository.get_server_by_slug(test_server_in_db.slug)


def test_clean_server_raise_server_busy(
    servers_repository: ServersRepository, test_server_in_db: Server
) -> None:
    servers_repository.update_server(
        server=test_server_in_db, status=ServerStatus.pending
    )
    with pytest.raises(ServerIsBusy):
        clean_server(servers_repository, test_server_in_db.slug)
