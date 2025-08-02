import unittest

from pyramide.form import Form
from pyramide.game_board import GameBoard
from pyramide.game_position import GamePosition


class TestForm(unittest.TestCase):
    def test_connected_form(self) -> None:
        positions = {GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)}
        form = Form(positions)
        self.assertEqual(len(form), 3)

    def test_disconnected_form_raises(self) -> None:
        positions = {GamePosition(0, 0), GamePosition(2, 2)}
        with self.assertRaises(AssertionError):
            Form(positions)

    def test_fits_on_board_true(self) -> None:
        board = GameBoard(
            {
                GamePosition(0, 0),
                GamePosition(1, 0),
                GamePosition(1, 1),
                GamePosition(2, 2),
            }
        )
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        self.assertTrue(form.fits_on_board(board))

    def test_fits_on_board_false(self) -> None:
        board = GameBoard({GamePosition(0, 0), GamePosition(2, 2)})
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        self.assertFalse(form.fits_on_board(board))

    def test_delete_from_board(self) -> None:
        board = GameBoard(
            {
                GamePosition(0, 0),
                GamePosition(1, 0),
                GamePosition(1, 1),
                GamePosition(2, 2),
            }
        )
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        results = set(form.delete_from_board(board))
        self.assertEqual(len(results), 1)
        self.assertEqual(next(iter(results))[0], GameBoard({GamePosition(2, 2)}))
        self.assertEqual(next(iter(results))[1], form.position_set)


if __name__ == "__main__":
    unittest.main()
