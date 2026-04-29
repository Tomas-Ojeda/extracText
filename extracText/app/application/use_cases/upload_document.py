from app.domain.document import Document
from app.domain.exceptions import DuplicateDocumentError, InvalidPDFError
from app.domain.repository import AbstractDocumentRepository
from app.infrastructure.services.pdf_extractor import validate_and_extract_text
from app.infrastructure.services.checksum_service import compute_checksum


class UploadDocumentUseCase:
    """Caso de uso: recibir un PDF en bytes, extraer texto y persistirlo."""

    def __init__(self, repository: AbstractDocumentRepository) -> None:
        self._repository = repository

    async def execute(self, filename: str, file_bytes: bytes) -> Document:
        """
        Raises:
            InvalidPDFError: si el archivo no es un PDF válido o supera el tamaño.
            DuplicateDocumentError: si ya existe un documento con el mismo checksum.
        """
        checksum = compute_checksum(file_bytes)

        existing = await self._repository.find_by_checksum(checksum)
        if existing:
            raise DuplicateDocumentError(checksum)

        text = validate_and_extract_text(file_bytes, filename)

        document = Document(filename=filename, content=text, checksum=checksum)
        return await self._repository.save(document)
