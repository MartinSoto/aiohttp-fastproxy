from aiohttp import web
from contextlib import asynccontextmanager
from dataclasses import dataclass

from yarl import URL


@dataclass
class AppInfo:
    app: web.Application = None
    url: URL = None


@asynccontextmanager
async def run_app(app: web.Application,
                  host: str = "0.0.0.0",
                  port: int = 8080) -> AppInfo:
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    try:
        yield AppInfo(app=app, url=URL(f"http://{host}:{port}/"))
    finally:
        await runner.cleanup()


@dataclass
class DownstreamAppInfo(AppInfo):
    request: web.Request = None
    body: str = None


@asynccontextmanager
async def downstream_app(*,
                         response: web.Response = None,
                         host: str = "0.0.0.0",
                         port: int = 9090) -> DownstreamAppInfo:
    request_info = DownstreamAppInfo()

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

    async with run_app(app, host=host, port=port) as app_info:
        request_info.app = app_info.app
        request_info.url = app_info.url
        yield request_info
