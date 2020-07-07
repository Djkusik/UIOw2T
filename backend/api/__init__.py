import logging
from aiohttp import web
from socketio import AsyncServer

from game import GameApp
from .routes import setup_routes
from .config import config


async def api_server(game_app: GameApp) -> web.AppRunner:
    app = web.Application()
    sio = AsyncServer()
    sio.attach(app)

    logging.basicConfig(level=logging.DEBUG)
    setup_routes(app, sio, game_app)
    await config(app, game_app)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    return runner
