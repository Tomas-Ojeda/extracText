from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel

from app.services.pdf_extractor import validate_and_extract_text

router = APIRouter(tags=["extract"])


class ExtractResponse(BaseModel):
    content: str


@router.post("/extract", response_model=ExtractResponse)
async def extract_text(file: UploadFile = File(...)):
    """Extrae el texto de un PDF validando extension y tamano."""
    file_bytes = await file.read()
    filename = file.filename or ""

    try:
        text = await run_in_threadpool(validate_and_extract_text, file_bytes, filename)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    return ExtractResponse(content=text)
