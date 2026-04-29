from app.infrastructure.services.checksum_service import compute_checksum


def test_checksum_is_sha256():
    data = b"hello world"
    result = compute_checksum(data)
    assert len(result) == 64  # SHA-256 produce 64 hex chars
    assert result == "b94d27b9934d3e08a52e52d7da7dabfac484efe04294e576db32ec3b3c2d0af9"


def test_same_data_same_checksum():
    data = b"contenido de prueba"
    assert compute_checksum(data) == compute_checksum(data)


def test_different_data_different_checksum():
    assert compute_checksum(b"aaa") != compute_checksum(b"bbb")
