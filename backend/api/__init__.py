import logging
from aiohttp import web
from socketio import AsyncServer

import game
from db import PlayerRankingRepository
from .routes import setup_routes


async def api_server(game_app: game.GameApp, sio: AsyncServer,
                     player_ranking_repository:PlayerRankingRepository) -> web.AppRunner:
    app = web.Application()
    sio.attach(app)

    logging.basicConfig(level=logging.DEBUG)
    setup_routes(app, sio, game_app, player_ranking_repository)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    return runner
