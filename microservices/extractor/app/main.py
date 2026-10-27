from fastapi import FastAPI

from app.api.router import api_router
from config.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.app_debug,
    )
    app.include_router(api_router)
    return app


app = create_app()


import signal


def _handle_shutdown(signum, frame):
    import sys
    sys.exit(0)


signal.signal(signal.SIGTERM, _handle_shutdown)
signal.signal(signal.SIGINT, _handle_shutdown)