from __future__ import annotations
from typing import Dict
from game.models.position import Position
import random


class Unit:
    range_penalty_multiplier = 0.2

    @staticmethod
    def make_from_prototype(unit_prototype: Dict) -> Unit:
        statistics = unit_prototype['statistics']

        return Unit(unit_prototype['name'], unit_prototype['category'], statistics['base_hp'],
                    statistics['base_phys_attack'], statistics['base_phys_defence'], statistics['base_mag_attack'],
                    statistics['base_mag_defence'], statistics['base_speed'], statistics['base_reach'])

    def __init__(self, name: str, category: str, hp: int,
                 phys_attack: int, phys_defence: int, mag_attack: int,
                 mag_defence: int, speed: int, reach: int) -> None:
        self.base_stats = {
            "hp": hp,
            "phys_attack": phys_attack,
            "phys_defence": phys_defence,
            "mag_attack": mag_attack,
            "mag_defence": mag_defence,
            "speed": speed,
            "reach": reach
        }
        self.name = name
        self.category = category

        self.stats = self.base_stats.copy()

        self.position = None
        self.target_map = None
        self.battle_logger = None

    # for resetting hp and temporal buffs/debuffs
    def reset_stats_to_base_values(self) -> None:
        self.stats = self.base_stats.copy()

    def set_target_map(self, target_map: 'TargetMap') -> None:
        self.target_map = target_map

    def set_position(self, position: Position) -> None:
        self.position = position

    def set_battle_logger(self, battle_logger: 'BattleLogger') -> None:
        self.battle_logger = battle_logger

    def attack(self) -> None:
        target: Unit = self.target_map.get_target_for(self)
        distance = self.position.distance_from(target.position)
        range_penalty = round(max(0, distance - self.stats["reach"]) * Unit.range_penalty_multiplier)

        self.battle_logger.set_attacker(self)
        self.battle_logger.set_defender(target)

        if self.stats["phys_attack"]:
            phys_attack_dmg = max(1, self.stats["phys_attack"] - range_penalty)
        else:
            phys_attack_dmg = 0

        if self.stats["mag_attack"]:
            mag_attack_dmg = max(1, self.stats["mag_attack"] - range_penalty)
        else:
            mag_attack_dmg = 0

        target.take_dmg(phys_attack_dmg, mag_attack_dmg)

    def take_dmg(self, phys_attack_dmg: int, mag_attack_dmg: int) -> None:

        # maybe use log functions for calculating mitigation?
        if phys_attack_dmg:
            phys_dmg_taken = max(1, phys_attack_dmg - self.stats["phys_defence"])
        else:
            phys_dmg_taken = 0

        if mag_attack_dmg:
            mag_dmg_taken = max(1, mag_attack_dmg - self.stats["mag_defence"])
        else:
            mag_dmg_taken = 0

        dmg_taken = (phys_dmg_taken + mag_dmg_taken)
        self.battle_logger.set_dmg_done(dmg_taken)

        self.stats["hp"] = self.stats["hp"] - dmg_taken

        if self.stats["hp"] <= 0:
            self.target_map.on_death(self)
            self.battle_logger.set_hp_left(0)
        else:
            self.battle_logger.set_hp_left(self.stats["hp"])

    def boost_stats(self, quiz_score):
        # If e.g. player scored 3 points in the quiz, we choose 3 of unit's stats (with repetition, so same stat can
        # be boosted many times) and add 1-3 to each of them
        for stat in random.choices(list(self.stats.keys()), k=quiz_score):
            self.stats[stat] += random.randint(0, quiz_score)

    def __hash__(self) -> int:
        return hash(
            (self.name, self.category, self.position,
             tuple(sorted(self.base_stats.items(), key=lambda x: x[0]))
             )
        )

    def __eq__(self, other: Unit):
        return type(other) is Unit and self.name == other.name and self.category == other.category and \
               self.base_stats == other.base_stats and self.position == other.position

    def __str__(self) -> str:
        return self.name + f", stats={self.stats}"
