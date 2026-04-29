from app.domain.document import Document
from app.domain.exceptions import DocumentNotFoundError
from app.domain.repository import AbstractDocumentRepository


class GetDocumentUseCase:
    def __init__(self, repository: AbstractDocumentRepository) -> None:
        self._repository = repository

    async def execute(self, document_id: str) -> Document:
        document = await self._repository.find_by_id(document_id)
        if not document:
            raise DocumentNotFoundError(document_id)
        return document
