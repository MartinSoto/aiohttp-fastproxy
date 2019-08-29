import aiohttp
from aiohttp import web

import pytest

from fastproxy import fastproxy

from . import utils


@pytest.yield_fixture
async def downstream_app(unused_tcp_port_factory):
    async with utils.downstream_app(
            port=unused_tcp_port_factory()) as app_info:
        yield app_info


@pytest.yield_fixture
async def proxy_app(unused_tcp_port_factory, downstream_app):
    proxy_app = web.Application()
    proxy_app.add_routes([
        web.route("*", "/{app_path:.*}",
                  fastproxy.make_proxy(proxy_app, downstream_app.url))
    ])

    async with utils.run_app(proxy_app,
                             port=unused_tcp_port_factory()) as app_info:
        yield app_info


@pytest.yield_fixture
async def http_client_session():
    async with aiohttp.ClientSession() as session:
        yield session
