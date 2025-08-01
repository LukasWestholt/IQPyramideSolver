import unittest

from src.Piece import GamePosition, Form, Piece, Color


class TestPieceFitsOnBoard(unittest.TestCase):
    def setUp(self):
        self.board = frozenset({
            GamePosition(x, y)
            for x in range(3)
            for y in range(3)
        })  # 3x3 grid

    def test_piece_fits1(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        piece = Piece(3, Color.green, form)
        self.assertTrue(piece.fits_on_board(self.board))

    def test_piece_fits2(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        piece = Piece(3, Color.green, form)
        board = frozenset({
            GamePosition(1, 2),
            GamePosition(2, 1),
            GamePosition(0, 0),
            GamePosition(2, 0),
            GamePosition(0, 2),
            GamePosition(2, 2)
        })
        # 90degres
        # it = piece.rotate_piece(90)
        # 2,2
        # 1,2
        # 2,1

        # print(piece.form.position_set)
        # print(board)
        # print(it.position_set)
        # for anchor in board:
        #     # Berechne die relative Verschiebung
        #     dx = anchor.x - max(pos.x for pos in it.position_set)
        #     dy = anchor.y - max(pos.y for pos in it.position_set)
        #
        #     # Verschiebe alle Positionen des Pieces
        #     translated_positions = {
        #         GamePosition(pos.x + dx, pos.y + dy)
        #         for pos in it.position_set
        #     }
        #
        #     print(translated_positions)
        #
        # print(Form(board))
        self.assertTrue(piece.fits_on_board(board))

    def test_piece_fits3(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        piece = Piece(3, Color.green, form)
        board = frozenset({GamePosition(0, 1), GamePosition(0, 0), GamePosition(2, 0), GamePosition(0, 2), GamePosition(2, 2), GamePosition(1, 0)})
        self.assertTrue(piece.fits_on_board(board))

    def test_piece_does_not_fit(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(3, 0)})
        piece = Piece(4, Color.red, form)
        self.assertFalse(piece.fits_on_board(self.board))

    def test_empty_board(self):
        form = Form({GamePosition(0, 0)})
        piece = Piece(1, Color.white, form)
        self.assertFalse(piece.fits_on_board(frozenset()))

    def test_exact_fit(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0)})
        piece = Piece(3, Color.blue, form)
        board = frozenset({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0)})
        self.assertTrue(piece.fits_on_board(board))

    def test_exact_fit_but_turned_form(self):
        form = Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(0, 2)})
        piece = Piece(3, Color.blue, form)
        board = frozenset({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0)})
        self.assertTrue(piece.fits_on_board(board))

    def test_piece_unfits_multiple_times(self):
        form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
        piece = Piece(3, Color.green, form)
        board = frozenset({
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
        piece = Piece(3, Color.green, form)
        new_boards = set(piece.delete_from_board(self.board))
        self.assertEqual(16, len(new_boards))
        for new_board, _ in new_boards:
            self.assertTrue(piece.fits_on_board(new_board), new_board)

if __name__ == "__main__":
    unittest.main()
