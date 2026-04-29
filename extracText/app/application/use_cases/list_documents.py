from app.domain.document import Document
from app.domain.repository import AbstractDocumentRepository


class ListDocumentsUseCase:
    def __init__(self, repository: AbstractDocumentRepository) -> None:
        self._repository = repository

    async def execute(self) -> list[Document]:
        return await self._repository.find_all()
