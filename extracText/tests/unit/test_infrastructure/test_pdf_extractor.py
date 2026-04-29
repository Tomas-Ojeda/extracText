import pytest
from app.domain.exceptions import InvalidPDFError
from app.infrastructure.services.pdf_extractor import validate_and_extract_text


def test_rejects_non_pdf_extension():
    with pytest.raises(InvalidPDFError, match="extensión .pdf"):
        validate_and_extract_text(b"data", "archivo.txt")


def test_rejects_oversized_file(monkeypatch):
    from config import settings as settings_module
    monkeypatch.setattr(settings_module.settings, "pdf_max_size_mb", 0)
    with pytest.raises(InvalidPDFError, match="tamaño máximo"):
        validate_and_extract_text(b"x" * 1024, "archivo.pdf")


def test_rejects_invalid_pdf_bytes():
    with pytest.raises(InvalidPDFError, match="válido"):
        validate_and_extract_text(b"esto no es un pdf", "archivo.pdf")
