import asyncio
import logging
import random
from typing import List, Tuple, Set


from game.models import Player
from game.game import Game
from game.waiting_room import WaitingRoom


class GameApp:
    def __init__(self) -> None:
        self.players: List[Player] = []
        self.waiting_room: WaitingRoom = WaitingRoom()
        self.current_games: List[Game] = []
        self.on_game_started = None
        self.on_battle_started = None
        self.on_game_result= None

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
                game = Game(players,self.on_game_started,self.on_battle_started,self.on_game_result)
                self.current_games.append(game)
                await game.set_on_game_started()

            await asyncio.sleep(5)
