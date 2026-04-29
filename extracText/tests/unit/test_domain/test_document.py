from datetime import datetime
from app.domain.document import Document


def test_document_creation():
    doc = Document(filename="test.pdf", content="Hola mundo", checksum="abc123")
    assert doc.filename == "test.pdf"
    assert doc.content == "Hola mundo"
    assert doc.checksum == "abc123"
    assert doc.id is None
    assert isinstance(doc.created_at, datetime)


def test_document_update_content():
    doc = Document(filename="test.pdf", content="original", checksum="abc")
    original_updated_at = doc.updated_at
    doc.update_content("nuevo contenido")
    assert doc.content == "nuevo contenido"
    assert doc.updated_at >= original_updated_at
