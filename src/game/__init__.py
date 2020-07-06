import asyncio
from typing import List
from uuid import UUID

from .player import Player


class Game:
    def __init__(self) -> None:
        self.players: List[Player] = []

    async def play(self) -> None:
        while True:
            await asyncio.sleep(2)

    def add_player(self, nick: str) -> UUID:
        id = next((player.id for player in self.players if player.nick == nick), None)
        if id is None:
            player = Player(nick)
            self.players.append(player)
            return player.id
        return id
