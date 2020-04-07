from enum import Enum
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    name: str
    username: str


class Project(BaseModel):
    name: str


class Commit(BaseModel):
    title: str
    message: Optional[str] = None


class ObjectAttributes(BaseModel):
    iid: int
    title: str
    merge_status: str
    url: str
    state: str
    last_commit: Commit


class Event(BaseModel):
    """Gitlab Event model"""

    object_kind: str
    user: User
    project: Project
    object_attributes: ObjectAttributes


class ServerStatus(str, Enum):  # noqa: WPS600
    stopped = "stopped"
    pending = "pending"
    running = "running"


class Server(BaseModel):
    """Primary backend model for docker-compose server instance"""

    slug: str

    branch_name: str
    status: ServerStatus = ServerStatus.stopped

    mr_id: Optional[int] = None
    mr_iid: Optional[int] = None
    mr_status: Optional[str] = None

    @property
    def is_busy(self) -> bool:
        return self.status == ServerStatus.pending
