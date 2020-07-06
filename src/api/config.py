from aiohttp import web

from src.game import Game


async def config(app: web.Application, game: Game):
    app["game"] = game


def get_game(request) -> Game:
    return request.app["game"]
