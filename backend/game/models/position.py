from __future__ import annotations


class Position:
    board_height = 8
    board_width = 8

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: Position):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    # all units will be located on the bottom half of the board during planning phase.
    # during simulation, one player`s units need to be mirrored to upper half.
    def get_mirrored_position(self) -> Position:
        x = Position.board_width - 1 - self.x
        y = Position.board_height - 1 - self.y

        return Position(x, y)

    def distance_from(self, position: Position) -> int:
        dist_x = abs(self.x - position.x)
        dist_y = abs(self.y - position.y)

        # maybe change metric later?
        return max(dist_x, dist_y)