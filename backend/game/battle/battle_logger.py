from typing import List, Dict
from game.models.unit import Unit
import logging


class BattleLogger:

    emptyItem: Dict = {
        'attacker_unit': None,
        'defender_unit': None,
        'dmg_done': None,
        'hp_left': None
    }

    def __init__(self):
        self.eventList: List = []
        self.currentItem: Dict = self.emptyItem.copy()

    def set_attacker(self, unit: Unit) -> None:
        self.currentItem['attacker_unit'] = str(unit)

    def set_defender(self, unit: Unit) -> None:
        self.currentItem['defender_unit'] = str(unit)

    def set_dmg_done(self, dmg: int) -> None:
        self.currentItem['dmg_done'] = dmg

    def set_hp_left(self, hp: int) -> None:
        self.currentItem['hp_left'] = hp
        self.add_to_event_list()

    def add_to_event_list(self) -> None:
        self.eventList.append(self.currentItem)
        self.currentItem = self.emptyItem.copy()

    def get_round_logs(self) -> str:
        logging.info("Battle logs:\n" + str(self.eventList))
        return self.eventList
