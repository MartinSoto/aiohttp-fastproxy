from aiohttp import web
from contextlib import asynccontextmanager
from dataclasses import dataclass


@asynccontextmanager
async def run_app(app, host="0.0.0.0", port=8080):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    try:
        yield app
    finally:
        await runner.cleanup()


@dataclass
class DownstreamAppRequestInfo:
    request: web.Request = None
    body: str = None


@asynccontextmanager
async def downstream_app(*,
                         response: web.Response = None,
                         host: str = "0.0.0.0",
                         port: int = 9090) -> DownstreamAppRequestInfo:
    request_info = DownstreamAppRequestInfo()

    if response is None:
        response = web.Response(text="Test response")

    async def handler(request: web.Request) -> web.Response:
        nonlocal response

        request_info.request = request.clone()
        request_info.body = await request.read()

        if response is None:
            raise Exception(
                "Each instance of the downstream test app can be called only once"
            )

        try:
            return response
        finally:
            response = None

    app = web.Application()
    app.add_routes([web.route("*", "/{path:.*}", handler)])

    async with run_app(app, host=host, port=port):
        yield request_info
