class DocumentNotFoundError(Exception):
    """Excepción cuando un documento no es encontrado."""
    pass


class DuplicateDocumentError(Exception):
    """Excepción cuando se intenta crear un documento duplicado."""
    pass
