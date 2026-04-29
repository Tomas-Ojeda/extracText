import pytest
from unittest.mock import AsyncMock
from app.application.use_cases.get_document import GetDocumentUseCase
from app.application.use_cases.delete_document import DeleteDocumentUseCase
from app.domain.document import Document
from app.domain.exceptions import DocumentNotFoundError


@pytest.fixture
def sample_document():
    return Document(id="abc123", filename="test.pdf", content="texto", checksum="chk")


@pytest.mark.asyncio
async def test_get_document_not_found():
    repo = AsyncMock()
    repo.find_by_id.return_value = None
    with pytest.raises(DocumentNotFoundError):
        await GetDocumentUseCase(repo).execute("id-inexistente")


@pytest.mark.asyncio
async def test_get_document_found(sample_document):
    repo = AsyncMock()
    repo.find_by_id.return_value = sample_document
    result = await GetDocumentUseCase(repo).execute("abc123")
    assert result.id == "abc123"


@pytest.mark.asyncio
async def test_delete_document_not_found():
    repo = AsyncMock()
    repo.delete.return_value = False
    with pytest.raises(DocumentNotFoundError):
        await DeleteDocumentUseCase(repo).execute("id-inexistente")
