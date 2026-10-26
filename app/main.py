from contextlib import asynccontextmanager

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.exception_handlers import register_exception_handlers
from app.api.router import api_router
from app.infrastructure.repositories.mongo_document_repository import MongoDocumentRepository
from app.infrastructure.services.checksum_service import Sha256ChecksumCalculator
from app.infrastructure.services.pdf_extractor import PdfTextExtractor
from config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestiona el ciclo de vida de MongoDB y el cableado de dependencias."""
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.mongodb_db_name]

    app.state.db = db
    app.state.repository = MongoDocumentRepository(db)
    app.state.text_extractor = PdfTextExtractor()
    app.state.checksum_calculator = Sha256ChecksumCalculator()

    yield
    client.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.app_debug,
        lifespan=lifespan,
    )
    register_exception_handlers(app)
    app.include_router(api_router)
    return app


app = create_app()