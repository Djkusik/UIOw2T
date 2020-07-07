import aiohttp_cors
from aiohttp import web


def get_cors(app: web.Application):
    return aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
