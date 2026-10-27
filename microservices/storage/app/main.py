import signal
from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.router import api_router
from app.infrastructure.repositories.mongo_document_repository import MongoDocumentRepository
from config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de la conexión a MongoDB."""
    client = AsyncIOMotorClient(settings.mongodb_url)
    app.state.db = client[settings.mongodb_db_name]
    try:
        await app.state.db[MongoDocumentRepository.COLLECTION].create_index("checksum", unique=True)
    except Exception as exc:
        raise RuntimeError(
            "No se pudo crear el índice único sobre 'checksum' en la colección 'documents'. "
            "Verifica que no haya checksums duplicados."
        ) from exc
    try:
        yield
    finally:
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


def _handle_shutdown(signum, frame):
    import sys
    sys.exit(0)


signal.signal(signal.SIGTERM, _handle_shutdown)
signal.signal(signal.SIGINT, _handle_shutdown)