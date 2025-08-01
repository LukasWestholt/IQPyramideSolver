from pyramide.GamePosition import GamePosition
from pyramide.Piece import Piece


class SolvedGame:
    def __init__(self, gameboard: frozenset[tuple[Piece, frozenset[GamePosition]]]):
        self.gameboard = gameboard
        assert len(self.gameboard) > 0

    def __hash__(self):
        return hash((self.gameboard,))

    def __eq__(self, other):
        if isinstance(other, SolvedGame):
            return self.gameboard == other.gameboard
        return False

    def __repr__(self):
        return f"<{self.__class__.__name__} with {self.gameboard}>"
