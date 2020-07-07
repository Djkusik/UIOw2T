from uuid import uuid4, UUID


class Player:
    def __init__(self, nick: str, id: str) -> None:
        self.nick: str = nick
        self.id: str = id
        self.in_game: bool = False
