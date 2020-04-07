from fastapi import Depends, HTTPException, Path
from starlette import status

from app.core.dependencies import get_repository
from app.core.repositories import EntityDoesNotExist
from app.severs.models import Server
from app.severs.repositories import ServersRepository


async def get_server_by_slug_from_path(
    slug: str = Path(..., min_length=1),
    servers_repo: ServersRepository = Depends(get_repository(ServersRepository)),
) -> Server:
    try:
        return servers_repo.get_server_by_slug(slug=slug)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Server does not exists",
        )
