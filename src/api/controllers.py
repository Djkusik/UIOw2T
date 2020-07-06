from aiohttp import web
from uuid import UUID

from .config import get_game


async def add_player(request):
    data = await request.post()
    nick = data.get("nick")
    if not nick:
        raise web.HTTPBadRequest(text="No nick")
    game = get_game(request)
    id: UUID = game.add_player(nick)
    return web.json_response(dict(id=str(id)))
