from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    DocumentNotFoundError,
    DuplicateDocumentError,
    InvalidPDFError,
)


def register_exception_handlers(app: FastAPI) -> None:
    """Traduce excepciones de dominio a respuestas HTTP."""

    @app.exception_handler(DocumentNotFoundError)
    async def document_not_found_handler(request: Request, exc: DocumentNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(DuplicateDocumentError)
    async def duplicate_document_handler(request: Request, exc: DuplicateDocumentError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidPDFError)
    async def invalid_pdf_handler(request: Request, exc: InvalidPDFError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": str(exc)},
        )