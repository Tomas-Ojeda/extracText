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
        """Actualiza el contenido del documento y la fecha de modificación."""
        self.content = new_content
        self.updated_at = datetime.now(UTC)
