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

    def rotate(self, angle: int) -> "Piece":
        """
        Rotates the piece by the specified angle in degrees.
        Supported angles are 0, 90, 180, and 270. Rotation is performed clockwise around the origin.

        0°: Returns the original form.
        90°: Rotates the piece 90 degrees clockwise.
        180°: Rotates the piece 180 degrees.
        270°: Rotates the piece 270 degrees clockwise.

        :raises ValueError: if the angle is not one of the supported values.
        """
        if angle == 0:
            return self
        elif angle == 90:
            return Piece(
                self.color,
                Form({GamePosition(-p.y, p.x) for p in self.form.position_set}),
            )
        elif angle == 180:
            return Piece(
                self.color,
                Form({GamePosition(-p.x, -p.y) for p in self.form.position_set}),
            )
        elif angle == 270:
            return Piece(
                self.color,
                Form({GamePosition(p.y, -p.x) for p in self.form.position_set}),
            )
        else:
            raise ValueError("Angle must be 0, 90, 180, or 270")

    def mirror(self, axis: str) -> "Piece":
        """
        Mirrors the piece along the specified axis.

        Supported axes are "x" (horizontal) and "y" (vertical).

        "x": Mirrors the piece across the horizontal axis (flips vertically).
        "y": Mirrors the piece across the vertical axis (flips horizontally).

        :raises ValueError: if the axis is not "x" or "y".
        """
        if axis == "x":
            return Piece(
                self.color,
                Form({GamePosition(p.x, -p.y) for p in self.form.position_set}),
            )
        elif axis == "y":
            return Piece(
                self.color,
                Form({GamePosition(-p.x, p.y) for p in self.form.position_set}),
            )
        else:
            raise ValueError("Axis must be 'horizontal' or 'vertical'")

    def all_transformations(self) -> set[Form]:
        transformations = set()
        for angle in [0, 90, 180, 270]:
            rotated = self.rotate(angle)
            transformations.add(rotated.form)
            transformations.add(rotated.mirror("x").form)
            transformations.add(rotated.mirror("y").form)
        return transformations

    def delete_from_board(
        self, board: GameBoard
    ) -> Iterator[tuple[GameBoard, frozenset[GamePosition]]]:
        for transformation in self.all_transformations():
            for new_board, placed_piece_position in transformation.delete_from_board(
                board
            ):
                yield new_board, placed_piece_position

    def fits_on_board(self, board: GameBoard) -> bool:
        try:
            next(self.delete_from_board(board))
            return True
        except StopIteration:
            return False
