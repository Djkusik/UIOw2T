import aiohttp_cors
from aiohttp import web

from src.game import WaitingRoom


async def config(app: web.Application, waiting_room: WaitingRoom):
    app["waiting_room"] = waiting_room


def get_waiting_room(request) -> WaitingRoom:
    return request.app["waiting_room"]


def get_cors(app: web.Application):
    return aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
