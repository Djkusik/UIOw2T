import random

from game.battle.target_map import TargetMap
from game.battle.battle_logger import BattleLogger
from game.models.unit import Unit
from game.player import Player
from typing import Tuple


class BattleSimulator:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1: Player = player1
        self.player2: Player = player2
        self.all_units = None

    def start_simulation(self, random_seed: int) -> Tuple[int, str, str]:
        random.seed(random_seed)
        for unit in self.player2.deployed_units:
            unit.set_position(unit.position.get_mirrored_position())

        self.player1.boost_units_with_quiz_score()
        self.player2.boost_units_with_quiz_score()

        target_map = TargetMap(self, self.player1.deployed_units, self.player2.deployed_units)
        battle_logger = BattleLogger()

        self.all_units = self.player1.deployed_units + self.player2.deployed_units
        random.shuffle(self.all_units)
        self.all_units = sorted(self.all_units, key=lambda unit: unit.stats["speed"], reverse=True)

        for unit in self.all_units:
            unit.set_target_map(target_map)
            unit.set_battle_logger(battle_logger)

        while True:
            for unit in self.all_units:
                if self.is_done():
                    return self.result(), self.get_final_message(), battle_logger.get_round_logs()
                unit.attack()

    def get_final_message(self):
        if self.result() == 0:
            message = "Draw"
        else:
            winner = self.player1.nick if self.result() > 0 else self.player2.nick
            message = f"Player '{winner}' won by {max(self.result(), -self.result())} units"
        return message

    def is_done(self) -> bool:
        return len(self.player1.deployed_units) == 0 or len(self.player2.deployed_units) == 0

    def result(self) -> int:
        return len(self.player1.deployed_units) - len(self.player2.deployed_units)

    def on_death(self, unit: Unit) -> None:
        index = self.all_units.index(unit)
        del self.all_units[index]
