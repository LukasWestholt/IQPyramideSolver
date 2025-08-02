from collections.abc import Iterator

from pyramide.GameBoard import GameBoard
from pyramide.GamePosition import GamePosition


class Form(GameBoard):
    def __init__(self, position_set: set[GamePosition] | frozenset[GamePosition]):
        normalized_position_set = GameBoard(position_set).normalize_to_gameboard().position_set
        super().__init__(normalized_position_set)
        self.assert_all_positions_connected()

    def get_anchor(self) -> GamePosition:
        return GamePosition(min(pos.x for pos in self.position_set), min(pos.y for pos in self.position_set))

    def delete_from_board(
        self, board: GameBoard
    ) -> Iterator[tuple[GameBoard, frozenset[GamePosition]]]:
        for anchor in board.position_set:
            for piece_point in self.position_set: # TODO
                # Berechne die relative Verschiebung, damit piece_point auf anchor liegt
                dx = anchor.x - piece_point.x
                dy = anchor.y - piece_point.y
                # Verschiebe alle Positionen des Pieces
                translated_positions = {
                    GamePosition(pos.x + dx, pos.y + dy)
                    for pos in self.position_set
                }
                # translated_positions = {
                #     pos + (anchor - piece_point)
                #     for pos in self.position_set
                # } TODO

                # Prüfe, ob alle verschobenen Positionen auf dem Spielbrett liegen
                if translated_positions.issubset(board.position_set):
                    yield GameBoard(board.position_set.difference(translated_positions)), frozenset(translated_positions)
                    break

    def fits_on_board(self, board: GameBoard) -> bool:
        try:
            next(self.delete_from_board(board))
            return True  # Das Piece passt
        except StopIteration:
            return False  # Kein gültiger Platz gefunden
