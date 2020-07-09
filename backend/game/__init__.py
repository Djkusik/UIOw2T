import asyncio
import logging
import random
from typing import List, Tuple, Set

from socketio import AsyncServer

from .battle.battle_simulator import BattleSimulator
from .models.position import Position
from .models.unit import Unit
from .player import Player
from api.route_constants import GAME_STARTED, GAME_RESULT


class WaitingRoom:
    def __init__(self, capacity: int = 2) -> None:
        self.players: Set[Player] = set()
        self.capacity = capacity

    def draw_two_players_to_game(self) -> Tuple[Player, Player]:
        players = random.sample(self.players, 2)
        for p in players:
            self.players.discard(p)
            p.in_game = True
        return players

    def join(self, player: Player):
        if not self.is_full() and player not in self.players:
            self.players.add(player)
            logging.info(f"Player '{player.nick}' joined waiting room")

    def leave(self, player: Player):
        if player in self.players:
            self.players.discard(player)
            logging.info(f"Player '{player.nick}' left waiting room")

    def is_full(self):
        return len(self.players) == self.capacity


class Game:
    def __init__(self, sio: AsyncServer, players: Tuple[Player, Player]) -> None:
        self._sio: AsyncServer = sio
        self.players: Tuple[Player, Player] = players
        self.is_finished = False

    def _get_nicks_of_players(self) -> Tuple[str, str]:
        return self.players[0].nick, self.players[1].nick

    async def wait_for_quiz_result(self):
        await asyncio.sleep(1)

    async def wait_for_units_spacing(self):
        await asyncio.sleep(1)

    async def battle(self) -> None:
        logging.info(
            "Start game of players: '%s' and '%s'" % self._get_nicks_of_players()
        )
        battle_simulator = BattleSimulator(*self.players)
        result, message, logs = battle_simulator.start_simulation(random_seed=17)
        logging.info(f"Battle result: {result}")
        self._end_game_for_players(message, logs)
        self.is_finished = True
        logging.info(
            "Finished game of players: '%s' and '%s'" % self._get_nicks_of_players()
        )

    def _end_game_for_players(self, message: str, logs: str) -> None:
        self.send_game_results(message, logs)
        for p in self.players:
            p.reset_after_game()

    def _all_players_connected(self):
        for player in self.players:
            if not player.in_game:
                return False
        return True

    async def set_on_game_started(self):
        if self._all_players_connected():
            message = {'message': 'game started'}
            for player in self.players:
                await self._sio.emit(GAME_STARTED, data=message, room=player.id)
                logging.info(f"Sent start game info to peer with SID: {player.id}")
        else:
            # end game if some player disconnected
            await self.send_game_results("Player disconnected, walkover", logs="")

    async def send_game_results(self, message: str, logs: str):
        for player in self.players:
            if player.in_game:
                await self._sio.emit(GAME_RESULT, data={
                    "message": {"msg": message, "logs": logs}
                }, room=player.id)
                logging.info(f"Sent game results info to peer with SID: {player.id}")


class GameApp:
    def __init__(self, sio: AsyncServer) -> None:
        self.players: List[Player] = []
        self.waiting_room: WaitingRoom = WaitingRoom()
        self.current_games: List[Game] = []
        self.sio: AsyncServer = sio

    def add_player(self, nick: str, id: str) -> Player:
        existing_player: Player = self.get_player_by_nick(nick)
        if existing_player:
            logging.info(f"Player '{existing_player.nick}' reconnected with id '{id}'")
            existing_player.reconnect(id)
            return existing_player

        new_player = Player(nick, id)
        self.players.append(new_player)
        self.waiting_room.join(new_player)
        return new_player

    def disconnect_player(self, player: Player):
        player.disconnect()
        self.waiting_room.leave(player)

    def get_players(self) -> List[Player]:
        return self.players

    def get_players_in_waiting_room(self) -> Set[Player]:
        return self.waiting_room.players

    def get_player_game(self, nick: str) -> Game:
        games = [g for g in self.current_games if nick in [p.nick for p in g.players]]
        if len(games) > 0:
            return games[len(games) - 1]

    def get_player_by_nick(self, nick: str) -> Player:
        return next((p for p in self.players if p.nick == nick), None)

    def get_player_by_id(self, id: str) -> Player:
        return next((p for p in self.players if p.id == id), None)

    def is_waiting_room_full(self):
        return self.waiting_room.is_full()

    async def start_games(self) -> None:
        while True:
            if self.is_waiting_room_full():
                players = self.waiting_room.draw_two_players_to_game()
                game = Game(self.sio, players)
                self.current_games.append(game)
                await game.set_on_game_started()
                await game.wait_for_quiz_result()
                await game.wait_for_units_spacing()
                await game.battle()
            await asyncio.sleep(5)
