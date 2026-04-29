import hashlib


def compute_checksum(data: bytes) -> str:
    """Calcula el checksum SHA-256 de los bytes recibidos.

    No se persiste el archivo en disco; opera directamente sobre los bytes en memoria.
    """
    return hashlib.sha256(data).hexdigest()
