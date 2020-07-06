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
        exist_player: Player = next((p for p in self.players if p.nick == nick), None)
        if exist_player:
            return exist_player.id
        new_player = Player(nick)
        self.players.append(new_player)
        return new_player.id
