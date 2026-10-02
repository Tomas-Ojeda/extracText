class DocumentNotFoundError(Exception):
    """Excepción cuando un documento no es encontrado."""
    pass


class DuplicateDocumentError(Exception):
    """Excepción cuando se intenta crear un documento duplicado."""
    pass


class InvalidPDFError(Exception):
    """Excepción cuando un PDF es inválido."""
    pass
