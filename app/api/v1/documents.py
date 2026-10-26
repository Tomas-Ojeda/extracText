from fastapi import APIRouter, Depends, UploadFile, File, status
from pydantic import BaseModel, ConfigDict

from app.application.use_cases.upload_document import UploadDocumentUseCase
from app.application.use_cases.get_document import GetDocumentUseCase
from app.application.use_cases.list_documents import ListDocumentsUseCase
from app.application.use_cases.update_document import UpdateDocumentUseCase
from app.application.use_cases.delete_document import DeleteDocumentUseCase
from app.api.dependencies import (
    get_checksum_calculator,
    get_repository,
    get_text_extractor,
)
from app.application.ports import ChecksumCalculator, TextExtractor
from app.domain.repository import AbstractDocumentRepository

router = APIRouter(prefix="/documents", tags=["documents"])


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename: str
    content: str
    checksum: str


class UpdateDocumentRequest(BaseModel):
    content: str


@router.post("/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    repository: AbstractDocumentRepository = Depends(get_repository),
    extractor: TextExtractor = Depends(get_text_extractor),
    checksum_calculator: ChecksumCalculator = Depends(get_checksum_calculator),
):
    """Recibe un PDF, extrae su texto y lo persiste."""
    file_bytes = await file.read()
    use_case = UploadDocumentUseCase(repository, extractor, checksum_calculator)
    return await use_case.execute(file.filename or "", file_bytes)


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    repository: AbstractDocumentRepository = Depends(get_repository),
):
    """Lista todos los documentos persistidos."""
    return await ListDocumentsUseCase(repository).execute()


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    repository: AbstractDocumentRepository = Depends(get_repository),
):
    """Obtiene un documento por su id."""
    return await GetDocumentUseCase(repository).execute(document_id)


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    body: UpdateDocumentRequest,
    repository: AbstractDocumentRepository = Depends(get_repository),
):
    """Actualiza el contenido de un documento."""
    return await UpdateDocumentUseCase(repository).execute(document_id, body.content)


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    repository: AbstractDocumentRepository = Depends(get_repository),
):
    """Elimina un documento por su id."""
    await DeleteDocumentUseCase(repository).execute(document_id)