import unittest
from game.shop.shop import Shop


class ShopTest(unittest.TestCase):

    def setUp(self):
        self.shop = Shop.get_instance()

    def test_singleton(self):
        """
        Test if singleton is working correctly and returning shop instance
        """
        self.assertIsInstance(self.shop, Shop)

    def test_prices(self):
        """
        Test if calculated prices of the units are correct with our math
        Calculated stats sum : {minimal price; maximal price}
        20-25   : {2; 3}
        26-32   : {4; 6}
        33-37   : {7; 10}
        37+     : {13; 13}
        """
        units = self.shop.units_list

        for unit in units:
            stats_sum = 0
            for stat in unit['statistics']:
                stats_sum += unit['statistics'][stat]
            stats_sum -= unit['statistics']['base_hp'] + int(round(unit['statistics']['base_hp'] / 10))

            if 20 <= stats_sum <= 25:
                self.assertIn(unit['price'], range(2, 4))
            if 26 <= stats_sum <= 32:
                self.assertIn(unit['price'], range(4, 7))
            if 33 <= stats_sum <= 37:
                self.assertIn(unit['price'], range(7, 11))
            if stats_sum > 37:
                self.assertEqual(unit['price'], 13)

    def test_random_units_amount(self):
        """
        Test if correct amount of units is returned
        """
        for i in range(1, 15):
            random_units_amount = len(self.shop.get_random_units(i, 5))
            self.assertTrue(random_units_amount, i)

    def test_random_units_currency_relation(self):
        """
        Test if correct amount of units is affordable from get_random_units
        """
        for i in range(2, 15):
            random_units = self.shop.get_random_units(6, i)
            affordable_units = 0
            for unit in random_units:
                if unit['price'] <= i:
                    affordable_units += 1
            self.assertGreaterEqual(affordable_units, 2)

    def test_affordable_units(self):
        """
        Test if units returned from get_affordable_units are always affordable
        """
        for i in range(2, 15):
            random_units = self.shop.get_affordable_units(i, 2)
            for unit in random_units:
                self.assertLessEqual(unit['price'], i)
