import logging
from aiohttp import web
from uuid import UUID

from .config import get_waiting_room


async def add_player(request):
    data = await request.post()
    nick = data.get("nick")
    if not nick:
        raise web.HTTPBadRequest(text="No nick")
    waiting_room = get_waiting_room(request)
    id: UUID = waiting_room.add_player(nick)
    logging.info("Create player with id %s" % id)
    return web.json_response(dict(id=str(id)))
