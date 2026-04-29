from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from pydantic import BaseModel

from app.application.use_cases.upload_document import UploadDocumentUseCase
from app.application.use_cases.get_document import GetDocumentUseCase
from app.application.use_cases.list_documents import ListDocumentsUseCase
from app.application.use_cases.update_document import UpdateDocumentUseCase
from app.application.use_cases.delete_document import DeleteDocumentUseCase
from app.domain.exceptions import (
    DocumentNotFoundError,
    DuplicateDocumentError,
    InvalidPDFError,
)
from app.api.dependencies import get_repository

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentResponse(BaseModel):
    id: str
    filename: str
    content: str
    checksum: str


class UpdateDocumentRequest(BaseModel):
    content: str


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    repository=Depends(get_repository),
):
    """Recibe un PDF, extrae su texto y lo persiste."""
    file_bytes = await file.read()
    use_case = UploadDocumentUseCase(repository)
    try:
        document = await use_case.execute(file.filename or "", file_bytes)
    except InvalidPDFError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except DuplicateDocumentError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        content=document.content,
        checksum=document.checksum,
    )


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(repository=Depends(get_repository)):
    """Lista todos los documentos persistidos."""
    documents = await ListDocumentsUseCase(repository).execute()
    return [
        DocumentResponse(id=d.id, filename=d.filename, content=d.content, checksum=d.checksum)
        for d in documents
    ]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, repository=Depends(get_repository)):
    """Obtiene un documento por su id."""
    try:
        document = await GetDocumentUseCase(repository).execute(document_id)
    except DocumentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return DocumentResponse(
        id=document.id, filename=document.filename,
        content=document.content, checksum=document.checksum,
    )


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    body: UpdateDocumentRequest,
    repository=Depends(get_repository),
):
    """Actualiza el contenido de un documento."""
    try:
        document = await UpdateDocumentUseCase(repository).execute(document_id, body.content)
    except DocumentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return DocumentResponse(
        id=document.id, filename=document.filename,
        content=document.content, checksum=document.checksum,
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: str, repository=Depends(get_repository)):
    """Elimina un documento por su id."""
    try:
        await DeleteDocumentUseCase(repository).execute(document_id)
    except DocumentNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
