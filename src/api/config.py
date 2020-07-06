import aiohttp_cors
from aiohttp import web

from src.game import Game


async def config(app: web.Application, game: Game):
    app["game"] = game


def get_game(request) -> Game:
    return request.app["game"]


def get_cors(app: web.Application):
    return aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*"
            )
        },
    )
