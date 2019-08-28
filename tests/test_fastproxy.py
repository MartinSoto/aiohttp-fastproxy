import aiohttp
import pytest

from .utils import run_app, downstream_app

from fastproxy.fastproxy import create_app

pytestmark = pytest.mark.asyncio


async def test_simple_get():
    async with downstream_app() as req_info:
        async with run_app(create_app()):
            async with aiohttp.ClientSession() as session:
                async with session.get('http://localhost:8080/') as resp:
                    assert req_info.request.method == "GET"
                    assert req_info.request.path == "/"
                    assert req_info.body == b""
                    assert await resp.text() == "Test response"
