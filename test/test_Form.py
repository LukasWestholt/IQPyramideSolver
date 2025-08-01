import unittest

from pyramide.Form import Form
from pyramide.GameBoard import GameBoard
from pyramide.GamePosition import GamePosition


class TestForm(unittest.TestCase):
    def test_connected_form(self):
        positions = {GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)}
        form = Form(positions)
        self.assertEqual(len(form), 3)

    def test_disconnected_form_raises(self):
        positions = {GamePosition(0, 0), GamePosition(2, 2)}
        with self.assertRaises(AssertionError):
            Form(positions)

    def test_fits_on_board_true(self):
        board = GameBoard({
            GamePosition(0, 0),
            GamePosition(1, 0),
            GamePosition(1, 1),
            GamePosition(2, 2)
        })
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        self.assertTrue(form.fits_on_board(board))

    def test_fits_on_board_false(self):
        board = GameBoard({
            GamePosition(0, 0),
            GamePosition(2, 2)
        })
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        self.assertFalse(form.fits_on_board(board))

    def test_delete_from_board(self):
        board = GameBoard({
            GamePosition(0, 0),
            GamePosition(1, 0),
            GamePosition(1, 1),
            GamePosition(2, 2)
        })
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        results = set(form.delete_from_board(board))
        self.assertEqual(len(results), 1)
        self.assertEqual(list(results)[0][0], GameBoard({GamePosition(2, 2)}))
        self.assertEqual(list(results)[0][1], form.position_set)

if __name__ == "__main__":
    unittest.main()
