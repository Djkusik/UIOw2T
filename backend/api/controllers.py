import json
import logging
import random

from aiofile import AIOFile

from db import PlayerRankingRepository
from game.models.position import Position
from game.models.unit import Unit
from socketio import AsyncServer
from .route_constants import *
from game import GameApp


class SocketController:
    def __init__(self, sio: AsyncServer, game_app: GameApp,player_ranking_repository:PlayerRankingRepository):
        self.sio: AsyncServer = sio
        self.game_app: GameApp = game_app
        self.player_ranking_repository = player_ranking_repository
        game_app.on_battle_started = self._on_battle_started
        game_app.on_game_started = self._on_game_started
        game_app.on_game_message = self._on_game_message

    async def _on_battle_started(self, players):
        await self.sio.emit(BATTLE_STARTED, data={
            "message": f"Battle between {players[0].nick} and {players[1].nick} started!"})

    async def _on_game_started(self, player):
        message = {'message': 'game started'}
        await self.sio.emit(GAME_STARTED, data=message, room=player.id)
        logging.info(f"Sent start game info to peer with SID: {player.id}")

    async def _on_game_message(self, message, logs, player):
        await self.sio.emit(GAME_RESULT, data={"message": message, "logs": logs}, room=player.id)

    async def units_ready(self, sid) -> None:
        await self.game_app.current_games[-1].save_what_is_ready(sid, what_is_ready="units")

    async def ranking(self, sid) -> None:
        ranking = self.player_ranking_repository.read_all()
        response = list(map(lambda player_rank: {"nick": player_rank[0], "rank":player_rank[1]}, ranking))
        await self.sio.emit(RANKING_REPLY, data=response)
        logging.info(f"Sent ranking to peer with SID: {sid}")

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

    async def get_units(self, sid):
        player = self.game_app.get_player_by_id(sid)
        units = player.deployed_units + [unit for unit in player.bench if unit is not None]
        response = list(map(lambda unit: unit.to_dict(), units))
        await self.sio.emit(GET_UNITS_REPLY, data=response)
        logging.info(f"Sent board state info to peer with SID: {sid}")

    async def get_gold(self, sid):
        player = self.game_app.get_player_by_id(sid)
        response = player.currency
        await self.sio.emit(GET_GOLD_REPLY, data=response)
        logging.info(f"Sent gold info to peer with SID: {sid}")

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

    async def get_question(self, sid, data):
        questions_path = "api/data/questions.json"
        classes = ['Warrior', 'Mage', 'Archer']
        question_class_association = [
            ['BD', 'JITP', 'UNIX', 'WDI'],
            ['Asem', 'MONT', 'PSI', 'SO', 'TA', 'TC', 'TK', 'TM', 'TO', 'TW'],
            ['AK', 'IO', 'SK', 'SR', 'ZO']
        ]

        try:
            unit_class = data['unit_class']
            class_id = classes.index(unit_class)
        except KeyError:
            await self.sio.emit(ERROR, data={"message": "no unit class provided"}, room=sid)
            return
        except ValueError:
            await self.sio.emit(ERROR, data={"message": "unknown unit class"}, room=sid)
            return

        logging.info(f"Getting question for {unit_class} (year {class_id})")

        async with AIOFile(questions_path, 'r') as f:
            s = await f.read()

        all_questions = json.loads(s)
        questions_for_class = \
            [question for question in all_questions if question['category'] in question_class_association[class_id]]

        response = random.choice(questions_for_class)
        await self.sio.emit(QUESTIONS_REPLY, data=response, room=sid)
        logging.info(f"Sent question to peer with SID: {sid}")

    async def save_question_score(self, sid, data):
        classes = ['Warrior', 'Mage', 'Archer']
        try:
            unit_class = data['unit_class']
            score = data['score']  # +-1
            class_id = classes.index(unit_class)
        except KeyError:
            await self.sio.emit(ERROR,
                    data={"message": "missing question score parameters ('unit_class' and 'score' needed"}, room=sid)
            return
        except ValueError:
            await self.sio.emit(ERROR, data={"message": "unknown unit class"}, room=sid)
            return

        player = self.game_app.get_player_by_id(sid)
        player.save_question_result(unit_class, score)
        logging.info(f"Saved question score {score} for class {unit_class} for player {player}")

        await self.sio.emit(SCORE_REPLY, data={"message": "Score saved"}, room=sid)
        await self.game_app.current_games[-1].save_what_is_ready(sid, what_is_ready="quiz")

    async def add_units(self, sid, data):
        if len(data) == 0:
            await self.sio.emit(ERROR, data={"message": "Empty units list"}, room=sid)
            return
        player = self.game_app.get_player_by_id(sid)

        for unit_data in data:
            unit = Unit.make_from_prototype(unit_data['unit'])
            x, y = unit_data['position'][0], unit_data['position'][1]
            unit.set_position(Position(x, y))
            player.deployed_units.append(unit)
            player.currency -= unit_data['unit']['price']
            logging.info(f"Added unit {unit} for player {player}")

        await self.sio.emit(ADD_UNITS_REPLY, data={"message": f"Units added for player {player.nick}"}, room=sid)

    async def get_shop_units(self, sid):
        player = self.game_app.get_player_by_id(sid)
        planning_phase_validator = player.on_planning_phase_start()
        offer = planning_phase_validator.get_offer()
        logging.info(f"Sent units from shop to peer with SID: {sid}")
        logging.info(f"Sent units: {offer}")
        await self.sio.emit(UNITS_FROM_SHOP_REPLY, data=offer, room=sid)
