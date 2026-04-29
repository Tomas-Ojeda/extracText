import io
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.domain.exceptions import InvalidPDFError
from config.settings import settings


def validate_and_extract_text(file_bytes: bytes, filename: str) -> str:
    """Valida el PDF y extrae su texto directamente desde memoria.

    Raises:
        InvalidPDFError: si el archivo no es PDF válido o supera el tamaño máximo.
    """
    if not filename.lower().endswith(".pdf"):
        raise InvalidPDFError("El archivo debe tener extensión .pdf")

    if len(file_bytes) > settings.pdf_max_size_bytes:
        raise InvalidPDFError(
            f"El archivo supera el tamaño máximo permitido de {settings.pdf_max_size_mb} MB."
        )

    try:
        reader = PdfReader(io.BytesIO(file_bytes))
    except PdfReadError:
        raise InvalidPDFError("El archivo no es un PDF válido.")

    text = "\n".join(
        page.extract_text() or "" for page in reader.pages
    ).strip()

    return text
