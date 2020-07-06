import logging
from aiohttp import web

from src.game import WaitingRoom
from .routes import setup_routes
from .config import config


async def api_server(waiting_room: WaitingRoom) -> web.AppRunner:
    app = web.Application()
    logging.basicConfig(level=logging.DEBUG)
    setup_routes(app)
    await config(app, waiting_room)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 8080)
    await site.start()
    return runner
