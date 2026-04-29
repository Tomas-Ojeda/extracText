class DocumentNotFoundError(Exception):
    """Se lanza cuando no se encuentra un documento en el repositorio."""

    def __init__(self, document_id: str) -> None:
        super().__init__(f"Documento con id '{document_id}' no encontrado.")
        self.document_id = document_id


class DuplicateDocumentError(Exception):
    """Se lanza cuando ya existe un documento con el mismo checksum."""

    def __init__(self, checksum: str) -> None:
        super().__init__(f"Ya existe un documento con checksum '{checksum}'.")
        self.checksum = checksum


class InvalidPDFError(Exception):
    """Se lanza cuando el archivo no es un PDF válido o supera el tamaño permitido."""
    pass
