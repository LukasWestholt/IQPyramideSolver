from dataclasses import dataclass


@dataclass(frozen=True)
class GamePosition:
    """(0, 0) is top left."""
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))
