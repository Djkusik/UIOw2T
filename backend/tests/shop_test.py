import unittest
from game.shop.shop import Shop


class ShopTest(unittest.TestCase):
    def test_singleton(self):
        shop = Shop.get_instance()
        self.assertIsInstance(shop, Shop)

    def test_prices(self):
        shop = Shop.get_instance()
        units = shop.units_list

        test_passed = True

        for unit in units:
            stats_sum = 0
            for stat in unit['statistics']:
                stats_sum += unit['statistics'][stat]
            stats_sum -= unit['statistics']['base_hp'] + int(round(unit['statistics']['base_hp'] / 10))

            if 20 <= stats_sum <= 25:
                if not 2 <= unit['price'] <= 3:
                    test_passed = False
            if 26 <= stats_sum <= 32:
                if not 4 <= unit['price'] <= 6:
                    test_passed = False
            if 33 <= stats_sum <= 37:
                if not 7 <= unit['price'] <= 10:
                    test_passed = False
            if stats_sum > 37:
                if not unit['price'] == 13:
                    test_passed = False

        self.assertTrue(test_passed)

    def test_random_units_amount(self):
        shop = Shop.get_instance()
        test_passed = True

        for i in range(1, 15):
            random_units_amount = len(shop.get_random_units(i, 5))
            if random_units_amount != i:
                test_passed = False

        self.assertTrue(test_passed)

    def test_random_units_currency_relation(self):
        shop = Shop.get_instance()
        test_passed = True

        for i in range(2, 15):
            random_units = shop.get_random_units(6, i)
            affordable_units = 0
            for unit in random_units:
                if unit['price'] <= i:
                    affordable_units += 1
            if affordable_units < 2:
                test_passed = False

        self.assertTrue(test_passed)

    def test_affordable_units(self):
        shop = Shop.get_instance()
        test_passed = True

        for i in range(2, 15):
            random_units = shop.get_affordable_units(i, 2)
            for unit in random_units:
                if unit['price'] > i:
                    test_passed = False

        self.assertTrue(test_passed)
