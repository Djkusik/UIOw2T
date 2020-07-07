from uuid import uuid4, UUID


class Player:
    def __init__(self, nick: str) -> None:
        self.id: UUID = uuid4()
        self.nick: str = nick
        self.in_game: bool = False
