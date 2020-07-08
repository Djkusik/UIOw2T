import json

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
        self.currentItem: Dict = self.emptyItem

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
        self.currentItem = self.emptyItem

    def send_turn_logs(self) -> None:
        # Think how to implement returning logs
        packed_json = json.dumps(self.eventList)
        logging.info("Battle logs: " + str(self.eventList))
        self.eventList = []
