from fastapi import APIRouter

from app.guard.routes import router as guard_router
from app.severs.routes import router as servers_router

router = APIRouter()

router.include_router(servers_router)
router.include_router(guard_router)
