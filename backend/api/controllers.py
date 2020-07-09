import copy
import json
import logging
import random

from aiofile import AIOFile
from game.models.position import Position
from game.models.unit import Unit
from socketio import AsyncServer
from .route_constants import *
from game import GameApp
from game.shop.shop import Shop

# TODO Unit store instead of this shit
UNITS = {
    "warrior": Unit('Gariusz', 'warrior', 30, 5, 5, 0, 3, 3, 3),
    "archer": Unit('Faliusz', 'archer', 15, 7, 2, 0, 1, 7, 8),
    "mage": Unit('Bartusz', 'mage', 10, 0, 0, 10, 7, 5, 6)
}


class SocketController:
    def __init__(self, sio: AsyncServer, game_app: GameApp):
        self.sio: AsyncServer = sio
        self.game_app: GameApp = game_app

    async def on_socket_connected(self, sid, environ):
        logging.info(f"Got new connection from peer with SID: {sid}")
        pass

    async def on_socket_disconnected(self, sid):
        logging.info(f"Disconnected from peer with SID: {sid}")
        player = self.game_app.get_player_by_id(sid)
        if player is not None:
            self.game_app.disconnect_player(player)

    async def on_socket_login(self, sid, data):
        if 'nick' not in data:
            await self.sio.emit(ERROR, data={"message": "no login specified"}, room=sid)
            return
        nick = data['nick']
        player = self.game_app.add_player(nick, sid)
        await self.sio.emit(LOGIN_REPLY, data={"message": "login ok"}, room=sid)
        logging.info(f"Added player '{player.nick}' with id '{player.id}' to the game")

    async def get_players(self, sid):
        players = self.game_app.get_players()
        response = dict(players=[p.nick for p in players])
        await self.sio.emit(PLAYERS_REPLY, data=response, room=sid)
        logging.info(f"Sent player info to peer with SID: {sid}")

    async def get_players_in_waiting_room(self, sid):
        players = self.game_app.get_players_in_waiting_room()
        response = dict(players_waiting=[p.nick for p in players])
        await self.sio.emit(PLAYERS_WAITING_REPLY, data=response, room=sid)
        logging.info(f"Sent waiting players info to peer with SID: {sid}")

    async def get_questions(self, sid, data):
        default_number = 3
        questions_path = "api/data/questions.json"

        # Get the requested number or use default
        num = data['num'] if 'num' in data else default_number
        logging.info(f"Getting {num} questions (default is {default_number})")
        try:
            num = int(num)
        except:
            num = default_number

        async with AIOFile(questions_path, 'r') as f:
            s = await f.read()
            questions = json.loads(s)
        response = random.sample(questions, num)
        await self.sio.emit(QUESTIONS_REPLY, data=response, room=sid)
        logging.info(f"Sent {num} questions to peer with SID: {sid}")

    async def save_quiz_score(self, sid, data):
        if "score" not in data:
            await self.sio.emit(ERROR, data={"message": "No quiz score provided"}, room=sid)
            return
        player = self.game_app.get_player_by_id(sid)
        player.quiz_score = data["score"]
        logging.info(f"Saved quiz score {data['score']} for player {player}")
        await self.sio.emit(SCORE_REPLY, data={"message": "Score saved"}, room=sid)

    async def add_unit(self, sid, data):
        if not _unit_data_check(data):
            await self.sio.emit(ERROR, data={"message": "Unit spec incorrect"}, room=sid)
            return
        player = self.game_app.get_player_by_id(sid)

        unit = copy.deepcopy(UNITS[data["class"]])
        x, y = data["position"]["x"], data["position"]["y"]
        unit.set_position(Position(x, y))

        player.deployed_units.append(unit)
        logging.info(f"Added unit {unit} for player {player}")
        await self.sio.emit(UNIT_REPLY, data={"message": f"Unit {unit} added"}, room=sid)

    async def get_shop_units(self, sid):
        player = self.game_app.get_player_by_id(sid)
        planning_phase_validator = player.on_planning_phase_start()
        offer = planning_phase_validator.get_offer()
        logging.info(f"Sent units from shop to peer with SID: {sid}")
        logging.info(f"Sent units: {offer}")
        await self.sio.emit(UNITS_FROM_SHOP_REPLY, data=offer, room=sid)



def _unit_data_check(data) -> bool:
    return (
            "class" in data and
            "position" in data and
            data["class"] in UNITS
            and "x" in data["position"]
            and "y" in data["position"]
    )
