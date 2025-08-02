import unittest

from pyramide.color import Color
from pyramide.form import Form
from pyramide.game import Game, NotValidProblemError
from pyramide.game_board import GameBoard
from pyramide.game_position import GamePosition
from pyramide.piece import Piece
from pyramide.solved_game import SolvedGame


class TestGameValidity(unittest.TestCase):
    def setUp(self) -> None:
        self.board = GameBoard(
            {GamePosition(x, y) for x in range(3) for y in range(3)}
        )  # 3x3 grid
        self.pieces = [
            Piece(
                Color.green,
                Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)}),
            )
        ]

    def test_game_is_valid1(self) -> None:
        Game(self.pieces, self.board, {})  # no exceptions

    def test_game_is_valid2(self) -> None:
        board = GameBoard(
            {GamePosition(x, y) for x in range(3) for y in range(3)}
            | {GamePosition(4, 0), GamePosition(4, 1), GamePosition(4, 2)}
        )
        Game(self.pieces, board, {})  # no exceptions

    def test_game_is_valid3(self) -> None:
        board = GameBoard(
            {GamePosition(x, y) for x in range(3) for y in range(3)}
            | {GamePosition(4, 0), GamePosition(4, 1)}
        )
        with self.assertRaises(NotValidProblemError):
            Game(self.pieces, board, {})


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self.board_positions = {
            GamePosition(0, 0),
            GamePosition(1, 0),
            GamePosition(2, 0),
            GamePosition(0, 1),
            GamePosition(1, 1),
            GamePosition(2, 1),
        }
        self.board = GameBoard(self.board_positions)

        form1 = Form({GamePosition(0, 0), GamePosition(1, 0)})
        form2 = Form({GamePosition(0, 0), GamePosition(0, 1)})

        self.piece1 = Piece(Color.red, form1)
        self.piece2 = Piece(Color.blue, form2)

        self.pieces = [self.piece1, self.piece2]

    def test_initial_state_is_empty(self) -> None:
        game = Game(self.pieces, self.board, {})
        self.assertEqual(game.state, {})

    def test_has_already_position(self) -> None:
        game = Game(
            self.pieces,
            self.board,
            {self.piece1: frozenset({GamePosition(0, 0), GamePosition(1, 0)})},
        )
        self.assertTrue(game.has_already_position(self.piece1))
        self.assertFalse(game.has_already_position(self.piece2))

    def test_is_valid_state(self) -> None:
        state = {
            self.piece1: frozenset({GamePosition(0, 0), GamePosition(1, 0)}),
            self.piece2: frozenset({GamePosition(2, 0), GamePosition(2, 1)}),
        }
        game = Game(self.pieces, self.board, state)
        self.assertTrue(game.is_valid_state())

    def test_get_new_state_merges_correctly(self) -> None:
        initial_state = {
            self.piece1: frozenset({GamePosition(0, 0), GamePosition(1, 0)})
        }
        game = Game(self.pieces, self.board, initial_state)
        new_state = game.get_new_state(
            {self.piece2: frozenset({GamePosition(2, 0), GamePosition(2, 1)})}
        )
        self.assertIn(self.piece1, new_state)
        self.assertIn(self.piece2, new_state)

    def test_is_valid_problem_true(self) -> None:
        Game(self.pieces, self.board, {})  # no exceptions

    def test_sort_pieces_by_size(self) -> None:
        game = Game(self.pieces, self.board, {})
        game.sort_pieces()
        self.assertGreaterEqual(len(game.pieces[0]), len(game.pieces[1]))

    def test_get_valid_gameboards_returns_solution(self) -> None:
        game = Game(self.pieces, self.board, {})
        result = game.solve(parallel=False)
        for r in result:
            self.assertIsInstance(r, SolvedGame)


if __name__ == "__main__":
    unittest.main()
