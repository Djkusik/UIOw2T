from typing import List, Dict

from game.models.position import Position
from game.models.unit import Unit
from game.shop.planning_phase_validator import PlanningPhaseValidator


class Player:
    BASE_INCOME = 5
    BASE_PLAYER_HP = 20
    BENCH_SIZE = 8
    # should increase throughout the game, change it later:
    MAX_UNITS_ON_BOARD = 9

    def __init__(self, nick: str, id: str) -> None:
        self.nick: str = nick
        self.id: str = id
        self.in_game: bool = False
        self.connected = True
        self.quiz_scores: Dict = {"Warrior": 0, "Mage": 0, "Archer": 0}
        self.deployed_units: List[Unit] = []
        self.bench: List[Unit] = [None] * Player.BENCH_SIZE
        self.hp: int = Player.BASE_PLAYER_HP
        self.currency: int = 0

    def disconnect(self):
        self.connected = False

    def reconnect(self, sid):
        self.connected = True
        self.id = sid

    def reset_after_game(self):
        self.deployed_units = []
        self.bench = [None] * Player.BENCH_SIZE
        self.in_game = False
        self.quiz_scores = {"Warrior": 0, "Mage": 0, "Archer": 0}
        self.currency = 0
        self.hp = Player.BASE_PLAYER_HP

    def save_question_result(self, unit_class: str, result: int):
        self.quiz_scores[unit_class] += result

    def boost_units_with_quiz_score(self):
        for unit in self.deployed_units:
            unit.boost_stats(self.quiz_scores[unit.category])

    def __str__(self) -> str:
        return f"Player(nick={self.nick}, id={self.id}, in_game={self.in_game}, units={self.deployed_units})"

    def calculate_income(self) -> int:
        # add win/loss streak or interest?
        return Player.BASE_INCOME

    def on_planning_phase_start(self) -> PlanningPhaseValidator:  # return value for testing
        self.currency += self.calculate_income()

        for unit in self.deployed_units:
            unit.reset_stats_to_base_values()

        for unit in self.bench:
            if unit is not None:
                unit.reset_stats_to_base_values()  # return value for testing

        return PlanningPhaseValidator(self)

    def on_battle_phase_end(self, result: int):
        if result == 0:
            # do sth on draw?
            pass
        elif result > 0:
            # do sth on victory?
            pass
        else:
            # do sth on defeat?
            self.hp += result
            if self.hp <= 0:
                # do sth on death?
                pass

    def get_free_bench_slots(self):
        return sum(unit is None for unit in self.bench)

    def add_unit(self, unit: Unit, price: int):
        self.currency -= price

        first_free_bench = self.bench.index(None)
        unit.set_position(Position(first_free_bench, -1))
        self.bench[first_free_bench] = unit
