from game.models.unit import Unit
from typing import List

class Player:
    NO_SCORE = -1

    def __init__(self, nick: str, id: str) -> None:
        self.nick: str = nick
        self.id: str = id
        self.in_game: bool = False
        self.quiz_score: int = Player.NO_SCORE
        self.units: List[Unit] = []

    def reset_after_game(self):
        self.units = []
        self.in_game = False
        self.quiz_score = Player.NO_SCORE

    def boost_units_with_quiz_score(self):
        for unit in self.units:
            unit.boost_stats(self.quiz_score)

    def __str__(self) -> str:
        return f"Player(nick={self.nick}, id={self.id}, in_game={self.in_game}, quiz_score={self.quiz_score}, units={self.units})"
