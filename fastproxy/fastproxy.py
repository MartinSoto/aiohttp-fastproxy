from aiohttp import web


async def writestr(response, str_val, sep='\n'):
    await response.write((str(str_val) + sep).encode('utf-8'))


async def proxy(request):
    response = web.StreamResponse()
    response.content_type = 'text/plain'
    await response.prepare(request)
    await writestr(response, request.method)
    await writestr(response, request.path)
    await writestr(response, dict(request.query))

    # request.content can be passed directly to a downstream request as the data parameter. See the client quickstart.
    await writestr(response, "--- Start of body ---")
    if request.can_read_body:
        async for chunk, is_end in request.content.iter_chunks():
            await response.write(chunk)
    await writestr(response, "\n--- End of body ---")

    await response.write_eof()

    return response


def create_app():
    app = web.Application()
    app.add_routes([web.route('*', '/{tail:.*}', proxy)])

    return app


if __name__ == '__main__':
    web.run_app(create_app())
