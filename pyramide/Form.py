from collections.abc import Iterator

from pyramide.GameBoard import GameBoard
from pyramide.GamePosition import GamePosition


class Form(GameBoard):
    def __init__(self, position_set: set[GamePosition] | frozenset[GamePosition]):
        super().__init__(position_set)
        self.assert_all_positions_connected()

    def normalize_to_form(self) -> "Form":
        return Form(self.normalize_to_gameboard().position_set)

    def delete_from_board(self, board: GameBoard) -> Iterator[tuple[GameBoard, frozenset[GamePosition]]]:
        for anchor in board.position_set:
            # Berechne die relative Verschiebung
            dx = anchor.x - min(pos.x for pos in self.position_set)
            dy = anchor.y - min(pos.y for pos in self.position_set)

            # Verschiebe alle Positionen des Pieces
            translated_positions = {
                GamePosition(pos.x + dx, pos.y + dy)
                for pos in self.position_set
            }

            # Prüfe, ob alle verschobenen Positionen auf dem Spielbrett liegen
            if translated_positions.issubset(board.position_set):
                yield GameBoard(board.position_set.difference(translated_positions)), frozenset(translated_positions)
            else:
                # Berechne die relative Verschiebung
                dx = anchor.x - max(pos.x for pos in self.position_set)
                dy = anchor.y - max(pos.y for pos in self.position_set)

                # Verschiebe alle Positionen des Pieces
                translated_positions = {
                    GamePosition(pos.x + dx, pos.y + dy)
                    for pos in self.position_set
                }

                # Prüfe, ob alle verschobenen Positionen auf dem Spielbrett liegen
                if translated_positions.issubset(board.position_set):
                    yield GameBoard(board.position_set.difference(translated_positions)), frozenset(translated_positions)

    def fits_on_board(self, board: GameBoard) -> bool:
        try:
            next(self.delete_from_board(board))
            return True  # Das Piece passt
        except StopIteration:
            return False  # Kein gültiger Platz gefunden
