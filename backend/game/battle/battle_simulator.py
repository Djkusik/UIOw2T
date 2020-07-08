import random

from typing import List

from game.battle.target_map import TargetMap
from game.battle.battle_logger import BattleLogger
from game.models.unit import Unit
from game.player import Player


class BattleSimulator:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1: Player = player1
        self.player2: Player = player2
        self.player1_unit_count: int = 0
        self.player2_unit_count: int = 0
        self.all_units = None

    def start_simulation(self, random_seed: int, player1_units: List[Unit], player2_units: List[Unit]) -> int:

        random.seed(random_seed)

        self.player1.units = player1_units.copy()
        self.player2.units = player2_units.copy()
        self.player1_unit_count = len(player1_units)
        self.player2_unit_count = len(player2_units)

        target_map = TargetMap(self, self.player1.units, self.player2.units)
        battle_logger = BattleLogger()

        self.all_units = self.player1.units + self.player2.units
        random.shuffle(self.all_units)
        self.all_units = sorted(self.all_units, key=lambda unit: unit.stats["speed"], reverse=True)

        for unit in self.all_units:
            unit.set_target_map(target_map)
            unit.set_battle_logger(battle_logger)

        self.player1.boost_units_with_quiz_score()
        self.player2.boost_units_with_quiz_score()

        while True:
            for unit in self.all_units:
                if self.is_done():
                    battle_logger.send_turn_logs()
                    return self.result()
                unit.attack()
            battle_logger.send_turn_logs()

    def is_done(self) -> bool:
        return self.player1_unit_count == 0 or self.player2_unit_count == 0

    def result(self) -> int:
        return self.player1_unit_count - self.player2_unit_count

    def on_death(self, unit: Unit) -> None:
        index = self.all_units.index(unit)
        del self.all_units[index]

        self.player1_unit_count = len(self.player1.units)
        self.player2_unit_count = len(self.player2.units)
