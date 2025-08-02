from dataclasses import dataclass


@dataclass(frozen=True)
class GamePosition:
    """(0, 0) is top left."""

    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __sub__(self, other: object) -> "GamePosition":
        if not isinstance(other, GamePosition):
            raise TypeError()
        return GamePosition(self.x - other.x, self.y - other.y)

    def __add__(self, other: object) -> "GamePosition":
        if not isinstance(other, GamePosition):
            raise TypeError()
        return GamePosition(self.x + other.x, self.y + other.y)
