from pyramide.game_position import GamePosition
from pyramide.piece import Piece


class SolvedGame:
    def __init__(
        self, gameboard: frozenset[tuple[Piece, frozenset[GamePosition]]]
    ) -> None:
        self.gameboard = gameboard
        assert len(self.gameboard) > 0

    def __hash__(self) -> int:
        return hash((self.gameboard,))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SolvedGame):
            return self.gameboard == other.gameboard
        return False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} with {self.gameboard}>"
