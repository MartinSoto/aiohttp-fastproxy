import aiohttp
from aiohttp import web


async def writestr(response, str_val, sep="\n"):
    await response.write((str(str_val) + sep).encode("utf-8"))


def make_proxy(app, base_url):
    client_sess = aiohttp.ClientSession()
    app.on_cleanup.append(lambda app: client_sess.close())

    async def proxy(request):
        target_url = base_url + request.path
        # request.content can be passed directly to a downstream request as the data parameter. See the client quickstart.

        remote_req_params = {}
        if request.can_read_body:
            remote_req_params["data"] = request.content

        async with client_sess.request(
            request.method, target_url, headers=request.headers, **remote_req_params
        ) as remote_response:
            response = web.StreamResponse(headers=remote_response.headers)
            await response.prepare(request)

            async for chunk, is_end in remote_response.content.iter_chunks():
                await response.write(chunk)

            await response.write_eof()

            return response

    return proxy


def create_app():
    app = web.Application()
    app.add_routes(
        [web.route("*", "/{tail:.*}", make_proxy(app, "http://localhost:9090"))]
    )

    return app


if __name__ == "__main__":
    web.run_app(create_app())
