import asyncio
import logging
import random
from typing import List, Tuple, Set
from socketio import AsyncServer

from .player import Player
from .battle.battle_simulator import BattleSimulator
from .models.position import Position
from .models.unit import Unit


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

    def is_full(self):
        return len(self.players) == self.capacity


class Game:
    def __init__(self, sio: AsyncServer, players: Tuple[Player, Player]) -> None:
        self.sio: AsyncServer = sio
        self.players: Tuple[Player, Player] = players
        self.is_finished = False

    def _get_nicks_of_players(self) -> Tuple[str, str]:
        return self.players[0].nick, self.players[1].nick

    async def wait_for_quiz_result(self):
        await asyncio.sleep(10)

    async def wait_for_units_spacing(self):
        await asyncio.sleep(10)

    async def battle(self) -> None:
        logging.info(
            "Start game of players: '%s' and '%s'" % self._get_nicks_of_players()
        )
        battle_simulator = BattleSimulator(*self.players)
        result = battle_simulator.start_simulation(random_seed=17)
        logging.info(f"Battle result: {result}")
        self._end_game_for_players()
        self.is_finished = True
        logging.info(
            "Finish game of players: '%s' and '%s'" % self._get_nicks_of_players()
        )

    def _end_game_for_players(self) -> None:
        for p in self.players:
            p.reset_after_game()

    async def set_on_game_started(self):
        message = {'message': 'game started'}
        for player in self.players:
            await self.sio.emit('game_started', data=message, room=player.id)
            logging.info(f"Sent start game info to peer with SID: {player.id}")

    async def send_game_results(self):
        message = {'message': []}
        for player in self.players:
            await self.sio.emit('game_results', data=message, room=player.id)
            logging.info(f"Sent game results info to peer with SID: {player.id}")


class GameApp:
    def __init__(self) -> None:
        self.players: List[Player] = []
        self.waiting_room: WaitingRoom = WaitingRoom()
        self.current_games: List[Game] = []
        self.sio: AsyncServer = None

    def add_player(self, nick: str, id: str) -> Player:
        existing_player: Player = self.get_player_by_nick(nick)
        if existing_player:
            return existing_player

        new_player = Player(nick, id)
        self.players.append(new_player)
        self.waiting_room.join(new_player)
        return new_player

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
                await game.send_game_results()
            await asyncio.sleep(5)
