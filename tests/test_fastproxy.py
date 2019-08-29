import pytest

pytestmark = pytest.mark.asyncio


async def test_simple_get(downstream_app, proxy_app, http_client_session):
    async with http_client_session.get(proxy_app.url) as resp:
        assert downstream_app.request.method == "GET"
        assert downstream_app.request.path == "/"
        assert downstream_app.body == b""
        assert await resp.text() == "Test response"


async def test_path_get(downstream_app, proxy_app, http_client_session):
    async with http_client_session.get(proxy_app.url / 'ze/path') as resp:
        assert downstream_app.request.method == "GET"
        assert downstream_app.request.path == "/ze/path"
        assert downstream_app.body == b""
        assert await resp.text() == "Test response"
