from starlette.concurrency import run_in_threadpool

from app.application.ports import ChecksumCalculator, TextExtractor
from app.domain.document import Document
from app.domain.exceptions import DuplicateDocumentError, InvalidPDFError
from app.domain.repository import AbstractDocumentRepository


class UploadDocumentUseCase:
    """Caso de uso: recibir un PDF en bytes, extraer texto y persistirlo."""

    def __init__(
        self,
        repository: AbstractDocumentRepository,
        extractor: TextExtractor,
        checksum_calculator: ChecksumCalculator,
    ) -> None:
        self._repository = repository
        self._extractor = extractor
        self._checksum = checksum_calculator

    async def execute(self, filename: str, file_bytes: bytes) -> Document:
        """
        Raises:
            InvalidPDFError: si el archivo no es un PDF válido o supera el tamaño.
            DuplicateDocumentError: si ya existe un documento con el mismo checksum.
        """
        checksum = self._checksum.compute(file_bytes)

        existing = await self._repository.find_by_checksum(checksum)
        if existing:
            raise DuplicateDocumentError(checksum)

        # CPU-bound (pypdf): se ejecuta en un thread aparte para no bloquear
        # el event loop de asyncio mientras procesa el PDF.
        text = await run_in_threadpool(self._extractor.extract, file_bytes, filename)

        document = Document(filename=filename, content=text, checksum=checksum)
        return await self._repository.save(document)