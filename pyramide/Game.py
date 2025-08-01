from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor

from tqdm import tqdm

from pyramide.GameBoard import GameBoard
from pyramide.GamePosition import GamePosition
from pyramide.Piece import Piece
from pyramide.SolvedGame import SolvedGame


class NotValidProblemException(Exception):
    pass

class Game:
    def __init__(self, pieces: list[Piece], board: GameBoard, state: dict[Piece, frozenset[GamePosition]]) -> None:
        self.pieces = pieces
        self.board = board
        self.state = state
        if not self._is_valid_problem():
            raise NotValidProblemException()

    def get_new_state(self, change: dict[Piece, frozenset[GamePosition]]) -> dict[Piece, frozenset[GamePosition]]:
        return {**change, **self.state}

    def has_already_position(self, piece: Piece) -> bool:
        return piece in self.state

    def is_valid_state(self) -> bool:
        return bool(all([piece in self.state for piece in self.pieces]))

    def _is_valid_problem(self) -> bool:
        """Heuristic for isolated spaces."""
        min_isolated_space = min((len(p) for p in self.pieces))
        return self.board.has_min_connected_gamepositions(min_isolated_space)

    def sort_pieces(self) -> None:
        self.pieces = sorted(self.pieces, key=lambda piece: len(piece), reverse=True)

    def process_position(self, args) -> frozenset[SolvedGame]:
        piece, possible_new_position, placed_piece_position = args
        try:
            new_game = Game(self.pieces, possible_new_position, self.get_new_state({piece: placed_piece_position}))
        except NotValidProblemException:
            return frozenset()
        return frozenset(new_game.solve())

    def solve(self, parallel=False) -> Iterator[SolvedGame]:
        for piece in self.pieces:
            if self.has_already_position(piece):
                continue

            tasks = (
                (piece, possible_new_position, placed_piece_position)
                for possible_new_position, placed_piece_position in piece.delete_from_board(self.board)
            )
            if parallel:
                prepared_tasks = tuple(tasks)
                with ProcessPoolExecutor() as executor:
                    iterator = tqdm(executor.map(self.process_position, prepared_tasks), total=len(prepared_tasks), desc=piece.color.value)
            else:
                iterator = map(self.process_position, tasks)
            for solvedGameSet in iterator:
                for solvedGame in solvedGameSet:
                    yield solvedGame
            return

        assert self.is_valid_state(), self.state
        yield SolvedGame(frozenset(self.state.items()))
