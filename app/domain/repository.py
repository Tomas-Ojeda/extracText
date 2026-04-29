from abc import ABC, abstractmethod
from app.domain.document import Document


class AbstractDocumentRepository(ABC):
    """Interface abstracta del repositorio de documentos (inversión de dependencias)."""

    @abstractmethod
    async def save(self, document: Document) -> Document:
        """Persiste un documento y retorna la entidad con el id asignado."""

    @abstractmethod
    async def find_by_id(self, document_id: str) -> Document | None:
        """Retorna un documento por su id, o None si no existe."""

    @abstractmethod
    async def find_by_checksum(self, checksum: str) -> Document | None:
        """Retorna un documento por su checksum, o None si no existe."""

    @abstractmethod
    async def find_all(self) -> list[Document]:
        """Retorna todos los documentos persistidos."""

    @abstractmethod
    async def update(self, document: Document) -> Document:
        """Actualiza un documento existente."""

    @abstractmethod
    async def delete(self, document_id: str) -> bool:
        """Elimina un documento. Retorna True si fue eliminado."""
