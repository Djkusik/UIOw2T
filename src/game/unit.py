from termcolor import colored

from game.position import Position

class Unit:

    range_penalty_multiplier = 0.2

    def __init__(self, hp: int, phys_attack: int, phys_defence: int,
                 mag_attack: int, mag_defence: int, speed: int, reach: int):

        self.base_hp = hp
        self.base_phys_attack = phys_attack
        self.base_phys_defenece = phys_defence
        self.base_mag_attack = mag_attack
        self.base_mag_defence = mag_defence
        self.base_speed = speed
        self.base_reach = reach

        self.hp = hp
        self.phys_attack = phys_attack
        self.phys_defence = phys_defence
        self.mag_attack = mag_attack
        self.mag_defence = mag_defence
        self.speed = speed
        self.reach = reach

        self.position = None
        self.targetMap = None

    # for resetting hp and temporal buffs/debuffs
    def reset_stats_to_base_values(self):
        self.hp = self.base_hp
        self.phys_attack = self.base_phys_attack
        self.phys_defence = self.base_phys_defenece
        self.mag_attack = self.base_mag_attack
        self.mag_defence = self.base_mag_defence
        self.speed = self.base_speed
        self.reach = self.base_reach

    def set_target_map(self, targetMap: 'TargetMap'):
        self.targetMap = targetMap

    def set_position(self, position: Position):
        self.position = position

    def attack(self):
        target: Unit = self.targetMap.get_target_for(self)
        distance = self.position.distance_from(target.position)
        range_penalty = int(round(max(0, distance - self.reach) * Unit.range_penalty_multiplier))

        if self.phys_attack:
            phys_attack_dmg = max(1, self.phys_attack - range_penalty)
        else:
            phys_attack_dmg = 0

        if self.mag_attack:
            mag_attack_dmg = max(1, self.mag_attack - range_penalty)
        else:
            mag_attack_dmg = 0

        target.take_dmg(phys_attack_dmg, mag_attack_dmg)

    def take_dmg(self, phys_attack_dmg: int, mag_attack_dmg: int):

        # maybe use log functions for calculating mitigation?
        if phys_attack_dmg:
            phys_dmg_taken = max(1, phys_attack_dmg - self.phys_defence)
        else:
            phys_dmg_taken = 0

        if mag_attack_dmg:
            mag_dmg_taken = max(1, mag_attack_dmg - self.mag_defence)
        else:
            mag_dmg_taken = 0

        self.hp = self.hp - (phys_dmg_taken + mag_dmg_taken)
        if self.hp <= 0:
            self.targetMap.on_death(self)


