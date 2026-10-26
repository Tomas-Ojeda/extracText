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


@pytest.mark.asyncio
async def test_upload_same_pdf_twice_returns_409(client: AsyncClient):
    with open("pdfs_variants/2020-Scrum-Guide-Spanish-Latin-South-American_v1.pdf", "rb") as f:
        pdf_bytes = f.read()

    r1 = await client.post("/api/v1/documents/", files={"file": ("scrum.pdf", pdf_bytes, "application/pdf")})
    r2 = await client.post("/api/v1/documents/", files={"file": ("scrum.pdf", pdf_bytes, "application/pdf")})

    assert r1.status_code == 201
    assert r2.status_code == 409