import asyncio
import logging
import random
from typing import List, Tuple, Set

from .player import Player


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
            p.quiz_score = Player.NO_SCORE


class GameApp:
    def __init__(self) -> None:
        self.players: List[Player] = []
        self.waiting_room: WaitingRoom = WaitingRoom()

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
                game = Game(players)
                await game.play()
                for p in players:
                    self.waiting_room.join(p)
            await asyncio.sleep(2)
