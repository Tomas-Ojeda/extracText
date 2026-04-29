import pytest
from unittest.mock import AsyncMock, MagicMock
from app.application.use_cases.upload_document import UploadDocumentUseCase
from app.domain.document import Document
from app.domain.exceptions import DuplicateDocumentError, InvalidPDFError


@pytest.fixture
def mock_repository():
    repo = AsyncMock()
    repo.find_by_checksum.return_value = None
    repo.save.side_effect = lambda doc: setattr(doc, "id", "mock-id") or doc
    return repo


@pytest.mark.asyncio
async def test_raises_duplicate_when_checksum_exists(mock_repository):
    mock_repository.find_by_checksum.return_value = MagicMock()
    use_case = UploadDocumentUseCase(mock_repository)
    with pytest.raises(DuplicateDocumentError):
        await use_case.execute("test.pdf", b"some bytes")


@pytest.mark.asyncio
async def test_raises_invalid_pdf_for_bad_file(mock_repository):
    use_case = UploadDocumentUseCase(mock_repository)
    with pytest.raises(InvalidPDFError):
        await use_case.execute("test.txt", b"not a pdf")
