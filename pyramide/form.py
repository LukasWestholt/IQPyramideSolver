from collections.abc import Iterator

from pyramide.game_board import GameBoard
from pyramide.game_position import GamePosition


class Form(GameBoard):
    def __init__(
        self, position_set: set[GamePosition] | frozenset[GamePosition]
    ) -> None:
        normalized_position_set = (
            GameBoard(position_set).normalize_to_gameboard().position_set
        )
        super().__init__(normalized_position_set)
        self.assert_all_positions_connected()
        self._anchor: GamePosition | None = None
        self._anchors: tuple[GamePosition, ...] | None = None

    def get_anchors(self) -> tuple[GamePosition, ...]:
        # get top left or all points
        if self._anchors is None:
            top_left = GamePosition(
                min(pos.x for pos in self.position_set),
                min(pos.y for pos in self.position_set),
            )
            if top_left in self.position_set:
                x: tuple[GamePosition, ...] = (top_left,)
            else:
                x = tuple(self.position_set)
            self._anchors = x
        return self._anchors

    def get_anchor(self) -> GamePosition:
        # get existing top left
        if self._anchor is None:
            top_left = GamePosition(0, 0)
            if top_left in self.position_set:
                self._anchor = top_left
            else:
                self._anchor = sorted(
                    self.position_set, key=lambda position: (position.y, position.x)
                )[0]
        return self._anchor

    def delete_from_board(
        self, board: GameBoard
    ) -> Iterator[tuple[GameBoard, frozenset[GamePosition]]]:
        piece_point = self.get_anchor()
        for anchor in board.position_set:
            # Berechne die relative Verschiebung, damit piece_point auf anchor liegt
            # Verschiebe alle Positionen des Pieces
            translated_positions = {
                pos + (anchor - piece_point) for pos in self.position_set
            }

            # Prüfe, ob alle verschobenen Positionen auf dem Spielbrett liegen
            if translated_positions.issubset(board.position_set):
                yield (
                    GameBoard(board.position_set.difference(translated_positions)),
                    frozenset(translated_positions),
                )

    def fits_on_board(self, board: GameBoard) -> bool:
        try:
            next(self.delete_from_board(board))
            return True  # Das Piece passt
        except StopIteration:
            return False  # Kein gültiger Platz gefunden
