import logging
from collections import Set
import random
from typing import Tuple

from .models import Player
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

