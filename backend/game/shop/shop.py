import json
import random

from typing import List, Dict, TextIO, Tuple
from math import exp, floor

class Shop:

    path_to_units_file: str = './game/data/units.json'

    def __init__(self):
        with open(self.path_to_units_file, 'r') as units_f:
            self.units_list = self.read_json(units_f)
        self.units_amount = len(self.units_list)
        self.add_prices()

    def read_json(self, file: TextIO) -> List[Dict]:
        return json.load(file)

    def add_prices(self):
        for unit in self.units_list:
            price = self.calculate_price(unit)

    def calculate_price(self, unit: Dict) -> int:
        stats_sum = 0
        for stat in unit['statistics']:
            stats_sum += unit['statistics'][stat]
        stats_sum -= unit['statistics']['base_hp'] + int(round(unit['statistics']['base_hp']/10))
        value = self.func(stats_sum)
        if value > 10:
            value = 13

        unit['price'] = value

    def func(self, x: int) -> int:
        # We need to think about costs, how much currency player is able to obtain?
        return int(round((-0.01729982 + 0.3214279 * exp(0.09289161 * x))))

    def get_random_units(self, quantity: int, currency: int) -> List[Dict]:
        # If player is too poor to afford anything, return total random
        if currency < 2:
            return random.sample(self.units_list, quantity)
        else:
            # Else random few random units and few affordable units
            units_to_return = []
            random_amount = int(floor(quantity * 2 / 3))
            units_to_return += random.choices(self.units_list, k=random_amount)
            units_to_return += self.get_affordable_units(currency, (quantity - random_amount))
            return units_to_return

    def get_affordable_units(self, currency: int, quantity: int) -> List:
        return random.choices([unit for unit in self.units_list if unit['price'] <= currency], k=quantity)

    def get_unit(self, name: str) -> Tuple['Unit', int]:
        for unit in self.units_list:
            if unit['name'] == name:
                return unit, unit['price']
