import aiohttp
from aiohttp import web
from yarl import URL


def make_proxy(app, base_url):
    base_url = URL(base_url)

    client_sess = aiohttp.ClientSession()
    app.on_cleanup.append(lambda app: client_sess.close())

    async def proxy(request):
        target_url = base_url / request.match_info["app_path"]

        remote_req_params = {}
        if request.can_read_body:
            remote_req_params["data"] = request.content

        async with client_sess.request(request.method,
                                       target_url,
                                       headers=request.headers,
                                       **remote_req_params) as remote_response:
            response = web.StreamResponse(headers=remote_response.headers)
            await response.prepare(request)

            async for chunk, is_end in remote_response.content.iter_chunks():
                await response.write(chunk)

            await response.write_eof()

            return response

    return proxy
