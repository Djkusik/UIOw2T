import random

from typing import List, Tuple

from termcolor import colored

from game.battle.targetMap import TargetMap
from game.unit import Unit


class BattleSimulator:
    def __init__(self):
        self.player1_units = None
        self.player2_units = None
        self.all_units = None
        self.iter = 0


    def start_simulation(self, randomSeed: int, player1_units: List[Unit], player2_units: List[Unit]) -> int:

        random.seed(randomSeed)

        self.player1_units = player1_units.copy()
        self.player2_units = player2_units.copy()

        targetMap = TargetMap(self, self.player1_units, self.player2_units)

        self.all_units = self.player1_units + self.player2_units
        random.shuffle(self.all_units)
        self.all_units = sorted(self.all_units, key=lambda unit: unit.speed, reverse=True)

        for unit in self.all_units:
            unit.set_target_map(targetMap)

        while True:
            done, result = self.check_done_and_result()
            if done:
                return result

            self.all_units[self.iter].attack()
            self.iter = (self.iter + 1) % len(self.all_units)

    def check_done_and_result(self) -> Tuple[bool, int]:
        player1_unit_count = len(self.player1_units)
        player2_unit_count = len(self.player2_units)

        done = player1_unit_count == 0 or player2_unit_count == 0
        result = player1_unit_count - player2_unit_count

        return done, result

    def on_death(self, unit: Unit):
        index = self.all_units.index(unit)
        del self.all_units[index]
        if index < self.iter:
            self.iter -= 1
