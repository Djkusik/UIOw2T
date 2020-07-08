class Player:
    def __init__(self, nick: str, id: str) -> None:
        self.nick: str = nick
        self.id: str = id
        self.in_game: bool = False
        self.quiz_score: int = -1

    def __str__(self) -> str:
        return f"Player(nick={self.nick}, id={self.id}, in_game={self.in_game}, quiz_score={self.quiz_score})"
