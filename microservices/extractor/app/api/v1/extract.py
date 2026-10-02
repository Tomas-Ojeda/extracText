from fastapi import APIRouter, HTTPException, UploadFile, File, status
from pydantic import BaseModel

from app.services.pdf_extractor import validate_and_extract_text
from app.services.checksum_service import compute_checksum

router = APIRouter(tags=["extract"])


class ExtractResponse(BaseModel):
    content: str
    checksum: str


@router.post("/extract", response_model=ExtractResponse)
async def extract_text(file: UploadFile = File(...)):
    """Extrae texto de un PDF y calcula su checksum."""
    file_bytes = await file.read()
    filename = file.filename or ""

    try:
        text = validate_and_extract_text(file_bytes, filename)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    checksum = compute_checksum(file_bytes)

    return ExtractResponse(content=text, checksum=checksum)
