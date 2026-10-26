import pytest
from app.main import create_app, lifespan


@pytest.mark.asyncio
async def test_lifespan_configures_state():
    app = create_app()
    async with lifespan(app):
        assert app.state.repository is not None
        assert app.state.text_extractor is not None
        assert app.state.checksum_calculator is not None