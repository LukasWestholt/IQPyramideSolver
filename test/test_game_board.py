import unittest

from pyramide.game_board import GameBoard
from pyramide.game_position import GamePosition


class TestGameBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.positions = {GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)}
        self.board = GameBoard(self.positions)

    def test_initialization(self) -> None:
        self.assertEqual(len(self.board), 3)
        self.assertIsInstance(self.board.position_set, frozenset)

    def test_equality(self) -> None:
        other_board = GameBoard(set(self.positions))
        self.assertEqual(self.board, other_board)

    def test_hash(self) -> None:
        board_set = {self.board}
        self.assertIn(GameBoard(self.positions), board_set)

    def test_str_representation(self) -> None:
        output = str(self.board)
        self.assertIn("#", output)
        self.assertIn(".", output)

    def test_get_neighbors(self) -> None:
        neighbors = self.board.get_neighbors(GamePosition(1, 0))
        expected = {GamePosition(0, 0), GamePosition(1, 1)}
        self.assertEqual(neighbors, expected)

    def test_assert_all_positions_connected_valid(self) -> None:
        # Should not raise an exception
        self.board.assert_all_positions_connected()

    def test_assert_all_positions_connected_invalid(self) -> None:
        disconnected = GameBoard({GamePosition(0, 0), GamePosition(5, 5)})
        with self.assertRaises(AssertionError):
            disconnected.assert_all_positions_connected()

    def test_normalize_to_gameboard(self) -> None:
        normalized = self.board.normalize_to_gameboard()
        expected_positions = {
            GamePosition(0, 0),
            GamePosition(1, 0),
            GamePosition(1, 1),
        }
        self.assertEqual(normalized.position_set, expected_positions)

    def test_has_min_connected_gamepositions_true(self) -> None:
        self.assertTrue(self.board.has_min_connected_gamepositions(2))

    def test_has_min_connected_gamepositions_false(self) -> None:
        board = GameBoard({GamePosition(0, 0), GamePosition(5, 5)})
        self.assertFalse(board.has_min_connected_gamepositions(2))


if __name__ == "__main__":
    unittest.main()
