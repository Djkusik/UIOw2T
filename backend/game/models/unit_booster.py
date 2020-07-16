class UnitBooster:

    boost_strategies = {
        'Archer': [('phys_attack', 3), ('phys_defence', 1), ('speed', 1), ('reach', 1)],
        'Warrior': [('phys_defence', 2), ('mag_defence', 2), ('hp', 2)],
        'Mage': [('mag_attack', 3), ('mag_defence', 3)]
    }

    @staticmethod
    def boost_unit(unit: 'Unit', quiz_score: int):
        unit_class = unit.category
        for stat, value in UnitBooster.boost_strategies[unit_class]:
            minimum = 0 if unit.stats[stat] == 0 else 1
            unit.stats[stat] = max(minimum, quiz_score * value)

