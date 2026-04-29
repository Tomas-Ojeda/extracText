from app.domain.exceptions import DocumentNotFoundError
from app.domain.repository import AbstractDocumentRepository


class DeleteDocumentUseCase:
    def __init__(self, repository: AbstractDocumentRepository) -> None:
        self._repository = repository

    async def execute(self, document_id: str) -> None:
        deleted = await self._repository.delete(document_id)
        if not deleted:
            raise DocumentNotFoundError(document_id)
