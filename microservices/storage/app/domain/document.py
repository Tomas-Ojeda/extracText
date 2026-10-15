from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class Document:
    """Entidad de dominio que representa un documento PDF procesado."""

    filename: str
    content: str
    checksum: str
    id: str | None = field(default=None)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def update_content(self, new_content: str) -> None:
        """Actualiza el contenido del documento y la fecha de modificacion."""
        self.content = new_content
        self.updated_at = datetime.now(UTC)


@dataclass
class DocumentSummary:
    """Resumen de un documento sin su contenido completo."""

    id: str
    filename: str
    checksum: str
    created_at: datetime
    updated_at: datetime