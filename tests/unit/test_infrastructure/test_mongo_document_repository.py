import pytest
from unittest.mock import AsyncMock, MagicMock

from bson import ObjectId
from datetime import datetime, timezone

from app.domain.document import Document
from app.infrastructure.repositories.mongo_document_repository import MongoDocumentRepository


@pytest.fixture
def repository():
    repo = MongoDocumentRepository(MagicMock())
    repo._collection = AsyncMock()
    return repo


def make_raw() -> dict:
    return {
        "_id": ObjectId(),
        "filename": "test.pdf",
        "content": "contenido de prueba",
        "checksum": "chk-123",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }


@pytest.mark.asyncio
async def test_save_sets_id(repository):
    doc = Document(filename="test.pdf", content="contenido", checksum="chk-123")
    result = MagicMock()
    result.inserted_id = ObjectId()
    repository._collection.insert_one = AsyncMock(return_value=result)

    saved = await repository.save(doc)

    assert saved.id == str(result.inserted_id)
    repository._collection.insert_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_find_by_id_invalid_returns_none(repository):
    assert await repository.find_by_id("id-no-valido") is None


@pytest.mark.asyncio
async def test_find_by_id_found(repository):
    raw = make_raw()
    repository._collection.find_one = AsyncMock(return_value=raw)

    found = await repository.find_by_id(str(raw["_id"]))

    assert found is not None
    assert found.content == "contenido de prueba"
    repository._collection.find_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_find_by_checksum_not_found(repository):
    repository._collection.find_one = AsyncMock(return_value=None)
    assert await repository.find_by_checksum("chk-inexistente") is None


@pytest.mark.asyncio
async def test_update_returns_document(repository):
    doc = Document(id=str(ObjectId()), filename="test.pdf", content="viejo", checksum="chk-123")
    repository._collection.update_one = AsyncMock()

    updated = await repository.update(doc)

    assert updated.content == "viejo"
    repository._collection.update_one.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_invalid_id_returns_false(repository):
    assert await repository.delete("id-no-valido") is False


@pytest.mark.asyncio
async def test_delete_returns_true(repository):
    result = MagicMock()
    result.deleted_count = 1
    repository._collection.delete_one = AsyncMock(return_value=result)
    assert await repository.delete(str(ObjectId())) is True