from typing import List, Optional

from app.core.schemas import RWSchema
from app.severs.models import Server, ServerStatus


class ServerForResponse(RWSchema, Server):
    """Server schema for http response"""


class ServerInResponse(RWSchema):
    server: ServerForResponse


class ServerInCreate(RWSchema):
    slug: str
    branch_name: str
    status: ServerStatus = ServerStatus.stopped
    mr_id: Optional[int] = None
    mr_iid: Optional[int] = None
    mr_status: Optional[str] = None


class ServerInUpdate(RWSchema):
    status: Optional[ServerStatus] = None
    branch_name: Optional[str] = None
    mr_id: Optional[int] = None
    mr_iid: Optional[int] = None
    mr_status: Optional[str] = None


class ListOfServersInResponse(RWSchema):
    servers: List[ServerForResponse]
    servers_count: int
