from typing import List

from game.models.unit import Unit
from game.shop.planning_phase_validator import PlanningPhaseValidator


class Player:
    NO_SCORE = -1
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
        self.quiz_score: int = Player.NO_SCORE
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
        self.quiz_score = Player.NO_SCORE
        self.currency = 0
        self.hp = Player.BASE_PLAYER_HP

    def boost_units_with_quiz_score(self):
        for unit in self.deployed_units:
            unit.boost_stats(self.quiz_score)

        for unit in self.bench:
            if unit is not None:
                unit.boost_stats(self.quiz_score)

    def __str__(self) -> str:
        return f"Player(nick={self.nick}, id={self.id}, in_game={self.in_game}, quiz_score={self.quiz_score}, units={self.deployed_units})"

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
        self.bench[first_free_bench] = unit
