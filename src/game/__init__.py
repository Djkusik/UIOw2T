import asyncio
import logging
import random
from typing import List, Tuple
from uuid import UUID

from .player import Player


class WaitingRoom:
    def __init__(self) -> None:
        self.players: List[Player] = []

    def draw_two_players_to_game(self) -> Tuple[Player, Player]:
        random.shuffle(self.players)
        players = (self.players.pop(), self.players.pop())
        for p in players:
            p.in_game = True
        return players

    def join(self, player: Player):
        self.players.append(player)
        logging.info("Player '%s' joined waiting room" % player.nick)


class Game:
    def __init__(self, players: Tuple[Player, Player]) -> None:
        self.players: Tuple[Player, Player] = players

    def _get_nicks_of_players(self) -> Tuple[str, str]:
        return self.players[0].nick, self.players[1].nick

    async def play(self) -> None:
        logging.info(
            "Start game of players: '%s' and '%s'" % self._get_nicks_of_players()
        )
        # Game
        self._end_game_for_players()
        logging.info(
            "Finish game of players: '%s' and '%s'" % self._get_nicks_of_players()
        )

    def _end_game_for_players(self) -> None:
        for p in self.players:
            p.in_game = False


class GameApp:
    def __init__(self) -> None:
        self.players: List[Player] = []
        self.waiting_room: WaitingRoom = WaitingRoom()

    def add_player(self, nick: str) -> UUID:
        exist_player: Player = self.get_player_by_nick(nick)
        if exist_player:
            return exist_player.id
        new_player = Player(nick)
        self.players.append(new_player)
        self.join_waiting_room(str(new_player.id))  # TODO remove it - it should be called during creating socket
        return new_player.id

    def get_player_by_nick(self, nick: str) -> Player:
        return next((p for p in self.players if p.nick == nick), None)

    def get_player_by_id(self, id: str) -> Player:
        return next((p for p in self.players if p.id == UUID(id)), None)

    def join_waiting_room(self, player_id: str):
        player = self.get_player_by_id(player_id)
        self.waiting_room.join(player)

    async def start_games(self) -> None:
        while True:
            if len(self.waiting_room.players) >= 2:
                players = self.waiting_room.draw_two_players_to_game()
                game = Game(players)
                await game.play()
                for p in players:
                    self.waiting_room.join(p)
            await asyncio.sleep(2)

