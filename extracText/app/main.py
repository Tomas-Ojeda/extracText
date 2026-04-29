from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.router import api_router
from config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la conexión a MongoDB."""
    client = AsyncIOMotorClient(settings.mongodb_url)
    app.state.db = client[settings.mongodb_db_name]
    yield
    client.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.app_debug,
        lifespan=lifespan,
    )
    app.include_router(api_router)
    return app


app = create_app()
