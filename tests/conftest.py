import pytest
from httpx import AsyncClient, ASGITransport
from mongomock_motor import AsyncMongoMockClient

from app.infrastructure.repositories.mongo_document_repository import MongoDocumentRepository
from app.infrastructure.services.checksum_service import Sha256ChecksumCalculator
from app.infrastructure.services.pdf_extractor import PdfTextExtractor
from app.main import create_app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def mock_db():
    """Base de datos MongoDB mockeada para tests."""
    client = AsyncMongoMockClient()
    return client["test_extractext"]


@pytest.fixture
async def app(mock_db):
    """Aplicación FastAPI con DB mockeada y dependencias cableadas."""
    application = create_app()
    application.state.db = mock_db
    application.state.repository = MongoDocumentRepository(mock_db)
    application.state.text_extractor = PdfTextExtractor()
    application.state.checksum_calculator = Sha256ChecksumCalculator()
    return application


@pytest.fixture
async def client(app):
    """Cliente HTTP de test."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac