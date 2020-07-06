import asyncio
import logging
import random
from typing import List, Tuple
from uuid import UUID

from .player import Player


class WaitingRoom:
    def __init__(self) -> None:
        self.players: List[Player] = []

    @property
    def players_not_in_game(self) -> List[Player]:
        return [p for p in self.players if not p.in_game]

    async def start_games(self) -> None:
        while True:
            if len(self.players_not_in_game) >= 2:
                players = self._draw_two_players_to_game()
                game = Game(players)
                await game.play()
            await asyncio.sleep(2)

    def _draw_two_players_to_game(self) -> Tuple[Player, Player]:
        players = random.sample(set(self.players_not_in_game), 2)
        for p in players:
            p.in_game = True
        return tuple(players)

    def add_player(self, nick: str) -> UUID:
        exist_player: Player = next((p for p in self.players if p.nick == nick), None)
        if exist_player:
            return exist_player.id
        new_player = Player(nick)
        self.players.append(new_player)
        return new_player.id


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
