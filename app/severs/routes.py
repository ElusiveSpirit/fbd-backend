from typing import Any, Dict

from fastapi import APIRouter, Body, Depends
from fastapi.responses import HTMLResponse
from starlette import status

from app.core.dependencies import get_repository
from app.severs.dependencies import get_server_by_slug_from_path
from app.severs.models import Server
from app.severs.repositories import ServersRepository
from app.severs.schemas import (
    ListOfServersInResponse,
    ServerForResponse,
    ServerInCreate,
    ServerInResponse,
    ServerInUpdate,
)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def read_root() -> HTMLResponse:
    with open("./frontend/index.html", "r") as index_file:
        html_resp = index_file.read()
        index_file.close()
        return HTMLResponse(content=html_resp)


@router.get(
    "/servers", response_model=ListOfServersInResponse, name="servers:list-servers"
)
def list_servers(
    servers_repo: ServersRepository = Depends(get_repository(ServersRepository)),
) -> ListOfServersInResponse:
    servers = servers_repo.get_servers_list()
    servers_for_response = [ServerForResponse.from_orm(server) for server in servers]
    return ListOfServersInResponse(
        servers=servers_for_response, servers_count=len(servers),
    )


@router.post(
    "/servers",
    status_code=status.HTTP_201_CREATED,
    response_model=ServerInResponse,
    name="servers:create-server",
)
async def create_new_server(
    server_create: ServerInCreate = Body(..., embed=True, alias="server"),
    servers_repo: ServersRepository = Depends(get_repository(ServersRepository)),
) -> ServerInResponse:
    server = servers_repo.create_server(
        slug=server_create.slug,
        branch_name=server_create.branch_name,
        status=server_create.status,
        mr_id=server_create.mr_id,
        mr_iid=server_create.mr_iid,
        mr_status=server_create.mr_status,
    )
    return ServerInResponse(server=ServerForResponse.from_orm(server))


@router.get(
    "/servers/{slug}", response_model=ServerInResponse, name="servers:get-server"
)
def retrieve_server_by_slug(
    server: Server = Depends(get_server_by_slug_from_path),
) -> ServerInResponse:
    return ServerInResponse(server=ServerForResponse.from_orm(server))


@router.delete("/servers/{slug}", name="servers:delete-server")
def delete_server_by_slug(
    server: Server = Depends(get_server_by_slug_from_path),
    servers_repo: ServersRepository = Depends(get_repository(ServersRepository)),
) -> None:
    servers_repo.delete_server(server=server)


@router.put(
    "/servers/{slug}", response_model=ServerInResponse, name="servers:update-server",
)
async def update_server_by_slug(
    server_update: ServerInUpdate = Body(..., embed=True, alias="server"),
    current_server: Server = Depends(get_server_by_slug_from_path),
    servers_repo: ServersRepository = Depends(get_repository(ServersRepository)),
) -> ServerInResponse:
    server = servers_repo.update_server(
        server=current_server,
        branch_name=server_update.branch_name,
        status=server_update.status,
        mr_id=server_update.mr_id,
        mr_iid=server_update.mr_iid,
        mr_status=server_update.mr_status,
    )
    return ServerInResponse(server=ServerForResponse.from_orm(server))


@router.post("/servers/{slug}/check")
def check_server_status_by_slug() -> Dict[str, Any]:
    """Check server in Gitlab and delete if MR closed"""
    return {}
