from app.domain.document import Document
from app.domain.exceptions import DocumentNotFoundError
from app.domain.repository import AbstractDocumentRepository


class UpdateDocumentUseCase:
    def __init__(self, repository: AbstractDocumentRepository) -> None:
        self._repository = repository

    async def execute(self, document_id: str, new_content: str) -> Document:
        document = await self._repository.find_by_id(document_id)
        if not document:
            raise DocumentNotFoundError(document_id)
        document.update_content(new_content)
        return await self._repository.update(document)
