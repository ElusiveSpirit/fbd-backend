from typing import List, Optional

from app.core.repositories import BaseRepository, EntityDoesNotExist, RepositoryException
from app.severs.models import Server, ServerStatus


class ServerIsBusy(RepositoryException):
    """Server is busy for update due to running ansible script"""


class ServersRepository(BaseRepository):
    redis_prefix = "servers"

    def create_server(  # noqa: WPS211
        self,
        *,
        slug: str,
        branch_name: str,
        status: ServerStatus = ServerStatus.stopped,
        mr_id: Optional[int] = None,
        mr_iid: Optional[int] = None,
        mr_status: Optional[str] = None,
    ) -> Server:
        created_server = Server(
            slug=slug,
            branch_name=branch_name,
            status=status,
            mr_id=mr_id,
            mr_iid=mr_iid,
            mr_status=mr_status,
        )

        key = self.get_redis_key_by_slug(created_server.slug)
        self._save(key, created_server.dict())
        return created_server

    def update_server(  # noqa: WPS211
        self,
        *,
        server: Server,
        branch_name: Optional[str] = None,
        status: Optional[ServerStatus] = None,
        mr_id: Optional[int] = None,
        mr_iid: Optional[int] = None,
        mr_status: Optional[str] = None,
    ) -> Server:
        updated_server = server.copy(deep=True)
        updated_server.branch_name = branch_name or server.branch_name
        updated_server.status = status or server.status
        updated_server.mr_id = mr_id or server.mr_id
        updated_server.mr_iid = mr_iid or server.mr_iid
        updated_server.mr_status = mr_status or server.mr_status

        key = self.get_redis_key_by_slug(updated_server.slug)
        self._save(key, updated_server.dict())
        return updated_server

    def get_server_by_slug(self, slug: str) -> Server:
        key = self.get_redis_key_by_slug(slug)
        server_data = self._get(key)
        if server_data is None:
            raise EntityDoesNotExist
        return Server(**server_data)

    def get_servers_list(self) -> List[Server]:
        raw_servers_list = self._get_list()
        return [Server(**server) for server in raw_servers_list]

    def delete_server(self, server: Server) -> None:
        key = self.get_redis_key_by_slug(server.slug)
        self._delete(key)
