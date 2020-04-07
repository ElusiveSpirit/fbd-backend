import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import DEBUG, PROJECT_NAME, VERSION
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.router import router as api_router

logger = logging.getLogger(__name__)


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(api_router)

    return application


app = get_application()
