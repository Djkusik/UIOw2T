from typing import List

from termcolor import colored

from game.unit import Unit


class TargetMap:
    def __init__(self, battle_simulator: 'BattleSimulator', player1_units: List[Unit], player2_units: List[Unit]):
        self.battle_simulator = battle_simulator
        self.player1_units = player1_units
        self.player2_units = player2_units

        self.map = {}

        for unit1 in player1_units:
            self.fill_map_for(unit1, player2_units)

        for unit2 in player2_units:
            self.fill_map_for(unit2, player1_units)

    def fill_map_for(self, unit: Unit, enemies: List[Unit]):
        if enemies:
            sorted_enemies = sorted(enemies, key=lambda enemy: unit.position.distance_from(enemy.position))
            self.map[unit] = sorted_enemies[0]

    def get_target_for(self, unit: Unit):
        return self.map[unit]

    def on_death(self, unit: Unit):
        if unit in self.player1_units:
            unit_allies = self.player1_units
            unit_enemies = self.player2_units
            self.player1_units.remove(unit)
        else:
            unit_allies = self.player2_units
            unit_enemies = self.player1_units
            self.player2_units.remove(unit)

        for enemy in unit_enemies:
            if self.get_target_for(enemy) == unit:
                self.fill_map_for(enemy, unit_allies)

        self.battle_simulator.on_death(unit)
