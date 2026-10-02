from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.domain.document import Document
from app.domain.exceptions import (
    DocumentNotFoundError,
    DuplicateDocumentError,
)
from app.domain.repository import AbstractDocumentRepository
from app.infrastructure.repositories.mongo_document_repository import MongoDocumentRepository

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentResponse(BaseModel):
    id: str
    filename: str
    content: str
    checksum: str


class CreateDocumentRequest(BaseModel):
    filename: str
    content: str
    checksum: str


class UpdateDocumentRequest(BaseModel):
    content: str


def get_repository(request) -> AbstractDocumentRepository:
    """Dependencia para obtener el repositorio de documentos."""
    return MongoDocumentRepository(request.app.state.db)


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def create_document(
    body: CreateDocumentRequest,
    repository: AbstractDocumentRepository = Depends(get_repository),
):
    """Crea un documento en la base de datos."""
    existing = await repository.find_by_checksum(body.checksum)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El documento ya existe (checksum duplicado)",
        )

    document = Document(
        filename=body.filename,
        content=body.content,
        checksum=body.checksum,
    )
    saved = await repository.save(document)

    return DocumentResponse(
        id=saved.id,
        filename=saved.filename,
        content=saved.content,
        checksum=saved.checksum,
    )


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    repository: AbstractDocumentRepository = Depends(get_repository),
):
    """Lista todos los documentos."""
    documents = await repository.find_all()
    return [
        DocumentResponse(id=d.id, filename=d.filename, content=d.content, checksum=d.checksum)
        for d in documents
    ]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    repository: AbstractDocumentRepository = Depends(get_repository),
):
    """Obtiene un documento por su id."""
    document = await repository.find_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado",
        )

    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        content=document.content,
        checksum=document.checksum,
    )


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    body: UpdateDocumentRequest,
    repository: AbstractDocumentRepository = Depends(get_repository),
):
    """Actualiza el contenido de un documento."""
    document = await repository.find_by_id(document_id)
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado",
        )

    document.update_content(body.content)
    updated = await repository.update(document)

    return DocumentResponse(
        id=updated.id,
        filename=updated.filename,
        content=updated.content,
        checksum=updated.checksum,
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    repository: AbstractDocumentRepository = Depends(get_repository),
):
    """Elimina un documento por su id."""
    deleted = await repository.delete(document_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado",
        )
