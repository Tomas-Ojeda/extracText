from datetime import datetime, UTC
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.document import Document
from app.domain.repository import AbstractDocumentRepository


class MongoDocumentRepository(AbstractDocumentRepository):
    """Implementación del repositorio usando MongoDB con Motor (async)."""

    COLLECTION = "documents"

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self._collection = db[self.COLLECTION]

    async def save(self, document: Document) -> Document:
        doc = _to_mongo(document)
        result = await self._collection.insert_one(doc)
        document.id = str(result.inserted_id)
        return document

    async def find_by_id(self, document_id: str) -> Document | None:
        if not ObjectId.is_valid(document_id):
            return None
        raw = await self._collection.find_one({"_id": ObjectId(document_id)})
        return _to_entity(raw) if raw else None

    async def find_by_checksum(self, checksum: str) -> Document | None:
        raw = await self._collection.find_one({"checksum": checksum})
        return _to_entity(raw) if raw else None

    async def find_all(self) -> list[Document]:
        cursor = self._collection.find()
        return [_to_entity(raw) async for raw in cursor]

    async def update(self, document: Document) -> Document:
        document.updated_at = datetime.now(UTC)
        await self._collection.update_one(
            {"_id": ObjectId(document.id)},
            {"$set": {"content": document.content, "updated_at": document.updated_at}},
        )
        return document

    async def delete(self, document_id: str) -> bool:
        if not ObjectId.is_valid(document_id):
            return False
        result = await self._collection.delete_one({"_id": ObjectId(document_id)})
        return result.deleted_count == 1


def _to_mongo(doc: Document) -> dict:
    return {
        "filename": doc.filename,
        "content": doc.content,
        "checksum": doc.checksum,
        "created_at": doc.created_at,
        "updated_at": doc.updated_at,
    }


def _to_entity(raw: dict) -> Document:
    return Document(
        id=str(raw["_id"]),
        filename=raw["filename"],
        content=raw["content"],
        checksum=raw["checksum"],
        created_at=raw["created_at"],
        updated_at=raw["updated_at"],
    )
