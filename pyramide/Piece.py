from collections.abc import Iterator

from pyramide.Color import Color
from pyramide.Form import Form
from pyramide.GameBoard import GameBoard
from pyramide.GamePosition import GamePosition


class Piece:
    def __init__(self, color: Color, form: Form):
        self.color = color
        self.form = form

    def __copy__(self):
        return Piece(self.color, Form(self.form.position_set))

    def __hash__(self):
        return hash((self.color, self.form))

    def __repr__(self):
        return f"<{self.__class__.__name__} with {(len(self), self.color)}>"

    def __eq__(self, other):
        if isinstance(other, Piece):
            return (self.color, self.form) == (other.color, other.form)
        return False

    def __len__(self):
        return len(self.form)

    def rotate_piece(self, angle: int) -> Form:
        if angle == 0:
            return self.form
        elif angle == 90:
            return Form({GamePosition(-p.y, p.x) for p in self.form.position_set})
        elif angle == 180:
            return Form({GamePosition(-p.x, -p.y) for p in self.form.position_set})
        elif angle == 270:
            return Form({GamePosition(p.y, -p.x) for p in self.form.position_set})
        else:
            raise ValueError("Angle must be 0, 90, 180, or 270")

    def mirror_piece(self, axis: str) -> "Piece":
        if axis == "x":
            return Piece(self.color, Form({GamePosition(p.x, -p.y) for p in self.form.position_set}))
        elif axis == "y":
            return Piece(self.color, Form({GamePosition(-p.x, p.y) for p in self.form.position_set}))
        else:
            raise ValueError("Axis must be 'horizontal' or 'vertical'")

    def delete_from_board(self, board: GameBoard) -> Iterator[tuple[GameBoard, frozenset[GamePosition]]]:
        for angle in [0, 90, 180, 270]:
            for new_board, placed_piece_position in self.rotate_piece(angle).delete_from_board(board):
                yield new_board, placed_piece_position

    def fits_on_board(self, board: GameBoard) -> bool:
        try:
            next(self.delete_from_board(board))
            return True
        except StopIteration:
            return False
