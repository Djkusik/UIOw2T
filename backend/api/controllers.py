import json
import logging
import random
from uuid import UUID

from aiofile import AIOFile
from aiohttp import web

from .config import get_game_app


async def add_player(request):
    data = await request.post()
    nick = data.get("nick")
    if not nick:
        raise web.HTTPBadRequest(text="No nick")
    game_app = get_game_app(request)
    id: UUID = game_app.add_player(nick)
    logging.info("Create player with id %s" % id)
    return web.json_response(dict(id=str(id)))


async def add_player_to_waiting_room(request):
    data = await request.post()
    id = data.get("id")
    if not id:
        raise web.HTTPBadRequest(text="No id")
    game_app = get_game_app(request)
    if not game_app.add_player_to_waiting_room(id):
        raise web.HTTPBadRequest(text="Player with given id doesn't exist")
    else:
        logging.info("Add player to waiting room with id %s" % id)
        return web.HTTPAccepted(text="OK")


async def get_players(request):
    game_app = get_game_app(request)
    players = game_app.get_players()
    return web.json_response(dict(players=[p.id for p in players]))


async def get_players_in_waiting_room(request):
    game_app = get_game_app(request)
    players_in_waiting_room = game_app.get_players_in_waiting_room()
    return web.json_response(dict(players=[p.id for p in players_in_waiting_room]))



async def get_questions(request):
    default_number = 3
    questions_path = "api/data/questions.json"
    # Get the requested number or use default
    num = request.rel_url.query.get("num")
    logging.info(f"Getting {num} questions (default is {default_number})")
    try:
        num = int(num)
    except:
        num = default_number

    async with AIOFile(questions_path, 'r') as f:
        s = await f.read()
        questions = json.loads(s)
    return web.json_response(random.sample(questions, num))
