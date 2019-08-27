from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, {}".format(request.match_info["name"]))


async def upload(request):
    total = 0
    if request.can_read_body:
        async for chunk, is_end in request.content.iter_chunks():
            total += len(chunk)

    return web.Response(text="Uploaded {} bytes".format(total))


def create_app():
    app = web.Application()
    app.add_routes([web.get("/{name}", hello)])
    app.add_routes([web.post("/upload", upload)])

    return app


if __name__ == "__main__":
    web.run_app(create_app())
