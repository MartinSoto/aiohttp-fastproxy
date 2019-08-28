import pytest

pytestmark = pytest.mark.asyncio


async def test_simple_get(proxy_app_setup, http_client_session):
    async with http_client_session.get('http://localhost:8080/') as resp:
        assert proxy_app_setup.request.method == "GET"
        assert proxy_app_setup.request.path == "/"
        assert proxy_app_setup.body == b""
        assert await resp.text() == "Test response"
