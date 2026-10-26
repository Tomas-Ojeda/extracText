import pytest
from unittest.mock import AsyncMock, MagicMock
from app.domain.document import Document
from app.application.use_cases.upload_document import UploadDocumentUseCase
from app.domain.exceptions import DuplicateDocumentError, InvalidPDFError


class FakeChecksum:
    def compute(self, data: bytes) -> str:
        return "checksum-fijo"


class FakeExtractor:
    def extract(self, data: bytes, filename: str) -> str:
        if not filename.endswith(".pdf"):
            raise InvalidPDFError("El archivo debe tener extensión .pdf")
        return "texto extraído"


@pytest.fixture
def mock_repository():
    repo = AsyncMock()
    repo.find_by_checksum.return_value = None
    repo.save.side_effect = lambda doc: setattr(doc, "id", "mock-id") or doc
    return repo


@pytest.mark.asyncio
async def test_raises_duplicate_when_checksum_exists(mock_repository):
    mock_repository.find_by_checksum.return_value = MagicMock()
    use_case = UploadDocumentUseCase(mock_repository, FakeExtractor(), FakeChecksum())
    with pytest.raises(DuplicateDocumentError):
        await use_case.execute("test.pdf", b"some bytes")


@pytest.mark.asyncio
async def test_raises_invalid_pdf_for_bad_file(mock_repository):
    use_case = UploadDocumentUseCase(mock_repository, FakeExtractor(), FakeChecksum())
    with pytest.raises(InvalidPDFError):
        await use_case.execute("test.txt", b"not a pdf")

@pytest.mark.asyncio
async def test_upload_happy_path_saves_document():
    repo = AsyncMock()
    repo.find_by_checksum.return_value = None
    saved = Document(filename="test.pdf", content="texto extraído", checksum="checksum-fijo")
    repo.save.return_value = saved

    use_case = UploadDocumentUseCase(repo, FakeExtractor(), FakeChecksum())
    result = await use_case.execute("test.pdf", b"some bytes")

    assert result.content == "texto extraído"
