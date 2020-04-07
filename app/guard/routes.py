from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.core.dependencies import get_repository
from app.guard.repositories import GuardRepository
from app.guard.services import get_public_access_status
from app.guard.tasks import close_public_access_task, open_public_access_task

router = APIRouter()


@router.get("/public", name="public:status")
def public_status(
    guard_repo: GuardRepository = Depends(get_repository(GuardRepository)),
) -> Dict[str, Any]:
    status = get_public_access_status(guard_repo)
    return {"opened": status}


@router.post("/public/open", name="public:open")
def open_public() -> None:
    open_public_access_task.delay()


@router.post("/public/close", name="public:close")
def close_public() -> None:
    close_public_access_task.delay()
