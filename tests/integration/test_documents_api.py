import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_list_documents_empty(client: AsyncClient):
    response = await client.get("/api/v1/documents/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_upload_non_pdf_returns_422(client: AsyncClient):
    response = await client.post(
        "/api/v1/documents/",
        files={"file": ("archivo.txt", b"contenido", "text/plain")},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_nonexistent_document_returns_404(client: AsyncClient):
    response = await client.get("/api/v1/documents/000000000000000000000000")
    assert response.status_code == 404
