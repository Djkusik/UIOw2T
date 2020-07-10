import logging

from typing import Tuple

from game.models import Player
from game.battle import BattleSimulator


class Game:
    def __init__(self, players: Tuple[Player, Player], on_game_started, on_battle_started,on_game_result) -> None:
        self.players: Tuple[Player, Player] = players
        self.is_finished = False
        self.players_quiz_and_units_ready = {p.id: {"units": False, "quiz": False} for p in self.players}
        self.on_game_started = on_game_started
        self.on_battle_started = on_battle_started
        self.on_game_result= on_game_result


    async def save_what_is_ready(self, sid, what_is_ready: str) -> None:
        if not (self.players[0].id == sid or self.players[1].id == sid):
            return
        player_id = self.players[0].id if self.players[0].id == sid else self.players[1].id
        logging.info(f"{player_id} has {what_is_ready} ready")
        self.players_quiz_and_units_ready[player_id][what_is_ready] = True
        await self.start_game_if_ready()

    async def start_game_if_ready(self) -> None:
        for dictionary in self.players_quiz_and_units_ready.values():
            for is_ready in dictionary.values():
                if not is_ready:
                    return
        await self.battle()

    def _get_nicks_of_players(self) -> Tuple[str, str]:
        return self.players[0].nick, self.players[1].nick

    async def battle(self) -> None:
        logging.info(
            "Start game of players: '%s' and '%s'" % self._get_nicks_of_players()
        )
        await self.on_battle_started(self.players)
        battle_simulator = BattleSimulator(*self.players)
        result, message, logs,winner = battle_simulator.start_simulation(random_seed=17)
        logging.info(f"Battle result: {result}")
        await self._end_game_for_players(message, logs)
        self.is_finished = True
        logging.info(
            "Finished game of players: '%s' and '%s'" % self._get_nicks_of_players()
        )

    async def _end_game_for_players(self, message: str, logs: str) -> None:
        await self.send_game_results(message, logs)
        for p in self.players:
            p.reset_after_game()

    def _all_players_connected(self):
        for player in self.players:
            if not player.in_game:
                return False
        return True



    async def set_on_game_started(self):
        if self._all_players_connected():
            for player in self.players:
                await self.on_game_started(player)
        else:
            # end game if some player disconnected
            await self.send_game_results("Player disconnected, walkover", logs="")

    async def send_game_results(self, message: str, logs: str):
        for player in self.players:
            if player.in_game:
                await self.on_game_result(message,logs,player)