from typing import Dict

from game.models.unit import Unit
from game.shop.buy_unit_excpetions import UnitNotInOfferException, FullBenchException, NotEnoughCurrencyException
from game.shop.shop import Shop


class PlanningPhaseValidator:
    OFFER_SIZE = 6

    def __init__(self, player: 'Player'):
        self.player = player

        shop = Shop.get_instance()
        self.offer = shop.get_random_units(PlanningPhaseValidator.OFFER_SIZE, player.currency)

        # send offer to display

    def buy_unit(self, unit_prototype: Dict):
        if unit_prototype not in self.offer:
            raise UnitNotInOfferException

        free_bench_slots = self.player.get_free_bench_slots()

        if free_bench_slots == 0:
            raise FullBenchException

        if unit_prototype['price'] > self.player.currency:
            raise NotEnoughCurrencyException

        self.offer.remove(unit_prototype)

        unit = Unit.make_from_prototype(unit_prototype)

        self.player.add_unit(unit, unit_prototype['price'])
