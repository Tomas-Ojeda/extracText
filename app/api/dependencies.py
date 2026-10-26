from fastapi import Request

from app.application.ports import ChecksumCalculator, TextExtractor
from app.domain.repository import AbstractDocumentRepository


async def get_repository(request: Request) -> AbstractDocumentRepository:
    """Provee el repositorio de documentos desde el estado de la app."""
    return request.app.state.repository


def get_text_extractor(request: Request) -> TextExtractor:
    """Provee el extractor de texto desde el estado de la app."""
    return request.app.state.text_extractor


def get_checksum_calculator(request: Request) -> ChecksumCalculator:
    """Provee el calculador de checksum desde el estado de la app."""
    return request.app.state.checksum_calculator