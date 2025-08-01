import unittest

from pyramide.Color import Color
from pyramide.Form import Form
from pyramide.GameBoard import GameBoard
from pyramide.GamePosition import GamePosition
from pyramide.Piece import Piece


class TestPieceFitsOnBoard(unittest.TestCase):
    def setUp(self):
        self.board = GameBoard({
            GamePosition(x, y)
            for x in range(3)
            for y in range(3)
        })  # 3x3 grid

    def test_piece_fits1(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        piece = Piece(Color.green, form)
        self.assertTrue(piece.fits_on_board(self.board))

    def test_piece_fits2(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        piece = Piece(Color.green, form)
        board = GameBoard({
            GamePosition(1, 2),
            GamePosition(2, 1),
            GamePosition(0, 0),
            GamePosition(2, 0),
            GamePosition(0, 2),
            GamePosition(2, 2)
        })
        self.assertTrue(piece.fits_on_board(board))

    def test_piece_fits3(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        piece = Piece(Color.green, form)
        board = GameBoard({GamePosition(0, 1), GamePosition(0, 0), GamePosition(2, 0), GamePosition(0, 2), GamePosition(2, 2), GamePosition(1, 0)})
        self.assertTrue(piece.fits_on_board(board))

    def test_piece_does_not_fit(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(3, 0)})
        piece = Piece(Color.red, form)
        self.assertFalse(piece.fits_on_board(self.board))

    def test_empty_board(self):
        form = Form({GamePosition(0, 0)})
        piece = Piece(Color.white, form)
        self.assertFalse(piece.fits_on_board(GameBoard(set())))

    def test_exact_fit(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0)})
        piece = Piece(Color.blue, form)
        board = GameBoard({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0)})
        self.assertTrue(piece.fits_on_board(board))

    def test_exact_fit_but_turned_form(self):
        form = Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(0, 2)})
        piece = Piece(Color.blue, form)
        board = GameBoard({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0)})
        self.assertTrue(piece.fits_on_board(board))

    def test_piece_unfits_multiple_times(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        piece = Piece(Color.green, form)
        board = GameBoard({
            GamePosition(x, y)
            for x in range(2)
            for y in range(2)
        })  # 2x2 grid
        new_boards = set(piece.delete_from_board(board))
        self.assertEqual(4, len(new_boards))
        for new_board, _ in new_boards:
            self.assertFalse(piece.fits_on_board(new_board), new_board)

    def test_piece_fits_multiple_times(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        piece = Piece(Color.green, form)
        new_boards = set(piece.delete_from_board(self.board))
        self.assertEqual(16, len(new_boards))
        for new_board, _ in new_boards:
            self.assertTrue(piece.fits_on_board(new_board), new_board)


class TestPiece(unittest.TestCase):
    def setUp(self):
        self.positions = {GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)}
        self.form = Form(self.positions)
        self.piece = Piece(Color.green, self.form)

    def test_initialization(self):
        self.assertEqual(len(self.piece), 3)
        self.assertEqual(self.piece.color, Color.green)
        self.assertEqual(len(self.piece.form), 3)

    def test_equality_and_hash(self):
        piece2 = Piece(Color.green, Form(self.positions))
        self.assertEqual(self.piece, piece2)
        self.assertEqual(hash(self.piece), hash(piece2))

    def test_copy(self):
        copy_piece = self.piece.__copy__()
        self.assertEqual(copy_piece, self.piece)
        self.assertIsNot(copy_piece, self.piece)

    def test_rotation_90(self):
        rotated = self.piece.rotate_piece(90)
        expected = Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(-1, 1)})
        self.assertEqual(rotated.position_set, expected.position_set)

    def test_rotation_180(self):
        rotated = self.piece.rotate_piece(180)
        expected = Form({GamePosition(0, 0), GamePosition(-1, 0), GamePosition(-1, -1)})
        self.assertEqual(rotated.position_set, expected.position_set)

    def test_rotation_270(self):
        rotated = self.piece.rotate_piece(270)
        expected = Form({GamePosition(0, 0), GamePosition(0, -1), GamePosition(1, -1)})
        self.assertEqual(rotated.position_set, expected.position_set)

    def test_invalid_rotation(self):
        with self.assertRaises(ValueError):
            self.piece.rotate_piece(45)

    def test_mirror_x(self):
        mirrored = self.piece.mirror_piece("x")
        expected = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, -1)})
        self.assertEqual(mirrored.form.position_set, expected.position_set)

    def test_mirror_y(self):
        mirrored = self.piece.mirror_piece("y")
        expected = Form({GamePosition(0, 0), GamePosition(-1, 0), GamePosition(-1, 1)})
        self.assertEqual(mirrored.form.position_set, expected.position_set)

    def test_invalid_mirror_axis(self):
        with self.assertRaises(ValueError):
            self.piece.mirror_piece("z")

    def test_fits_on_board_true(self):
        board = GameBoard({
            GamePosition(2, 2),
            GamePosition(3, 2),
            GamePosition(3, 3),
        })
        self.assertTrue(self.piece.fits_on_board(board))

    def test_fits_on_board_false(self):
        board = GameBoard({
            GamePosition(0, 0),
            GamePosition(2, 2),
        })
        self.assertFalse(self.piece.fits_on_board(board))

    def test_delete_from_board(self):
        board = GameBoard({
            GamePosition(2, 2),
            GamePosition(3, 2),
            GamePosition(3, 3),
        })
        results = list(self.piece.delete_from_board(board))
        self.assertTrue(any(isinstance(r, tuple) and len(r) == 2 for r in results))

if __name__ == "__main__":
    unittest.main()
