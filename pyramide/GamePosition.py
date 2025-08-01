from dataclasses import dataclass


@dataclass(frozen=True)
class GamePosition:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))
