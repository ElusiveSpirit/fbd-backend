import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from redis import Redis

from app.severs.models import Server
from app.severs.repositories import ServersRepository
from tests.testing_helpers import FakeRedisConnectionPool


@pytest.fixture
def app() -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    app = get_application()
    app.state.pool = FakeRedisConnectionPool()
    return app


@pytest.fixture
def pool() -> FakeRedisConnectionPool:
    return FakeRedisConnectionPool()


@pytest.fixture(autouse=True)
def client(app: FastAPI) -> TestClient:
    with TestClient(app) as client:
        yield client


@pytest.fixture
def servers_repository(app: FastAPI) -> ServersRepository:
    redis: Redis = app.state.pool.get_redis()
    repository = ServersRepository(redis=redis)
    return repository


@pytest.fixture
def test_server() -> Server:
    return Server(slug="server-slug", branch_name="server-branch-name",)


@pytest.fixture
def test_server_in_db(
    test_server: Server, servers_repository: ServersRepository
) -> Server:
    return servers_repository.create_server(**test_server.dict())
