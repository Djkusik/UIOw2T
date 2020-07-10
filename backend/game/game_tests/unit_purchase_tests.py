import unittest
import random

from game.models.unit import Unit
from game.player import Player
from game.shop.buy_unit_exceptions import FullBenchException, NotEnoughCurrencyException, UnitNotInOfferException


class UnitPurchaseTests(unittest.TestCase):

    def setUp(self):
        random.seed(0)
        self.player = Player('xd', '0')
        self.validator = self.player.on_planning_phase_start()

    #def test_check_offer(self):
    #    for unit in self.validator.offer:
    #        print(unit['name'], unit['price'])

    def test_simple_buy(self):
        prototype = self.validator.offer[1]
        expected_unit = Unit.make_from_prototype(prototype)

        self.validator.buy_unit(prototype)

        self.assertEqual(expected_unit, self.player.bench[0])

    def test_bench_full_exception(self):
        prototype = self.validator.offer[1]
        unit = Unit.make_from_prototype(prototype)
        for i in range(self.player.BENCH_SIZE):
            self.player.bench[i] = unit

        with self.assertRaises(FullBenchException):
            self.validator.buy_unit(prototype)


    def test_not_enough_currency_exception(self):
        prototype = self.validator.offer[0]
        with self.assertRaises(NotEnoughCurrencyException):
            self.validator.buy_unit(prototype)

        self.assertEqual(self.player.bench[0], None)

    def test_unit_not_in_offer_exception(self):
        self.player.currency = 13
        prototype = self.validator.offer[0]
        expected_unit = Unit.make_from_prototype(prototype)
        self.validator.buy_unit(prototype)

        with self.assertRaises(UnitNotInOfferException):
            self.validator.buy_unit(prototype)

        self.assertEqual(self.player.bench[0], expected_unit)
        self.assertEqual(self.player.bench[1], None)


