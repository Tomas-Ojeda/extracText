from fastapi import Request
from app.infrastructure.repositories.mongo_document_repository import MongoDocumentRepository


async def get_repository(request: Request) -> MongoDocumentRepository:
    """Provee el repositorio de documentos desde el estado de la app."""
    return MongoDocumentRepository(request.app.state.db)
