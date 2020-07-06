from aiohttp import web

from src.game import Game
from .routes import setup_routes
from .config import config


async def api_server(game: Game) -> web.AppRunner:
    app = web.Application()
    setup_routes(app)
    await config(app, game)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 8080)
    await site.start()
    return runner
