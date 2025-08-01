from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor

from pyramide.GameBoard import GameBoard
from pyramide.GameBoardGUI import GameBoardGUI
from pyramide.GamePosition import GamePosition
from pyramide.Piece import Piece


class Game:
    def __init__(self, pieces: list[Piece], board: GameBoard, state: dict[Piece, frozenset[GamePosition]]) -> None:
        self.pieces = pieces
        self.board = board
        self.state = state

    def get_new_state(self, change: dict[Piece, frozenset[GamePosition]]) -> dict[Piece, frozenset[GamePosition]]:
        return {**change, **self.state}

    def has_already_position(self, piece: Piece) -> bool:
        return piece in self.state

    def is_valid_state(self) -> bool:
        return bool(all([piece in self.state for piece in self.pieces]))

    def is_valid_problem(self) -> bool:
        """Heuristic for isolated spaces."""
        min_isolated_space = min((len(p) for p in self.pieces))
        return self.board.has_min_connected_gamepositions(min_isolated_space)

    def sort_pieces(self) -> None:
        self.pieces = sorted(self.pieces, key=lambda piece: len(piece), reverse=True)

    def process_position(self, args) -> frozenset[frozenset[tuple[Piece, frozenset[GamePosition]]]]:
        piece, possible_new_position, placed_piece_position = args
        new_game = Game(self.pieces, possible_new_position, self.get_new_state({piece: placed_piece_position}))
        if new_game.is_valid_problem():
            return frozenset(new_game.get_valid_gameboards())
        return frozenset()

    def get_valid_gameboards(self, parallel=False) -> Iterator[frozenset[tuple[Piece, frozenset[GamePosition]]]]:
        for piece in self.pieces:
            if self.has_already_position(piece):
                continue

            tasks = (
                (piece, possible_new_position, placed_piece_position)
                for possible_new_position, placed_piece_position in piece.delete_from_board(self.board)
            )

            with ProcessPoolExecutor(max_workers=4 if parallel else 1) as executor:
                results = executor.map(self.process_position, tasks)
                for result in results:
                    for valid_gameboard in result:
                        yield valid_gameboard
                    # output.update(result)
            return
            # return frozenset(output)

        assert self.is_valid_state(), self.state
        # output.add(frozenset(self.state.items()))
        yield frozenset(self.state.items())

        # return frozenset(output)
