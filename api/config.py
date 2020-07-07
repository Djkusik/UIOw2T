import aiohttp_cors
from aiohttp import web

from game import GameApp


async def config(app: web.Application, game_app: GameApp):
    app["game_app"] = game_app


def get_game_app(request) -> GameApp:
    return request.app["game_app"]


def get_cors(app: web.Application):
    return aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
