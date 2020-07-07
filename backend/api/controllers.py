import logging
import json
import random
from aiohttp import web
from uuid import UUID

from .config import get_game_app


async def add_player(request):
    data = await request.post()
    nick = data.get("nick")
    if not nick:
        raise web.HTTPBadRequest(text="No nick")
    waiting_room = get_game_app(request)
    id: UUID = waiting_room.add_player(nick)
    logging.info("Create player with id %s" % id)
    return web.json_response(dict(id=str(id)))


async def get_questions(request):
    default_number = 3
    questions_path = "api/data/questions.json"

    data = await request.post()
    num = data.get("num") if "num" in data else request.rel_url.query.get("num")
    logging.info(f"Getting {num} questions")
    try:
        num = int(num)
    except:
        num = default_number

    with open(questions_path, 'r') as f:
        questions = json.load(f)
    return web.json_response(random.sample(questions, num))
