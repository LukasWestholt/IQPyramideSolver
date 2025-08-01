import tkinter as tk
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from tkinter import font
import math


class Color(Enum):
    violet = "darkviolet"
    white = "white"
    brightGreen = "springgreen"
    green = "forestgreen"
    red = "red"
    orange = "orange"
    grey = "grey"
    yellow = "yellow"
    blue = "blue"
    pink = "pink"
    brightBlue = "royalblue"


@dataclass(frozen=True)
class GamePosition:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

class Form:
    def __init__(self, position_set: set[GamePosition] | frozenset[GamePosition]):
        self.position_set = frozenset(position_set)
        # self.assert_all_positions_connected() # TODO

    def __len__(self):
        return len(self.position_set)

    def __hash__(self):
        return hash((self.position_set,))

    def __eq__(self, other):
        if isinstance(other, Form):
            return self.position_set == other.position_set
        return False

    def __repr__(self):
        return f"<{self.__class__.__name__} with {set(self.position_set)}>"

    def __str__(self):
        if not self.position_set:
            return "<empty form>"

        min_x = min(p.x for p in self.position_set)
        max_x = max(p.x for p in self.position_set)
        min_y = min(p.y for p in self.position_set)
        max_y = max(p.y for p in self.position_set)

        rows = []
        rows.append("-" * (max_y - min_y + 1))
        for y in range(max_y, min_y - 1, -1):
            row = ""
            for x in range(min_x, max_x + 1):
                if GamePosition(x, y) in self.position_set:
                    row += "#"
                else:
                    row += "."
            rows.append(row)
        rows.append("-" * (max_y - min_y + 1))
        return "\n".join(rows)


    def assert_all_positions_connected(self):
        if not self.position_set:
            return None

        visited: set[GamePosition] = set()
        queue = deque([set(self.position_set).pop()])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            # Check 4-directional neighbors
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                neighbor = GamePosition(current.x + dx, current.y + dy)
                if neighbor in self.position_set and neighbor not in visited:
                    queue.append(neighbor)

        assert len(visited) == len(self.position_set), f"{self.position_set} has a Problem: {self.position_set.symmetric_difference(visited)}"
        return None

    def normalize(self) -> "Form":
        min_x = min(p.x for p in self.position_set)
        min_y = min(p.y for p in self.position_set)
        return Form({GamePosition(p.x - min_x, p.y - min_y) for p in self.position_set})

    def delete_from_board(self, board: frozenset[GamePosition]) -> Iterator[tuple[frozenset[GamePosition], frozenset[GamePosition]]]:
        for anchor in board:
            # Berechne die relative Verschiebung
            dx = anchor.x - min(pos.x for pos in self.position_set)
            dy = anchor.y - min(pos.y for pos in self.position_set)

            # Verschiebe alle Positionen des Pieces
            translated_positions = {
                GamePosition(pos.x + dx, pos.y + dy)
                for pos in self.position_set
            }

            # Prüfe, ob alle verschobenen Positionen auf dem Spielbrett liegen
            if translated_positions.issubset(board):
                yield board.difference(translated_positions), frozenset(translated_positions)
            else:
                # Berechne die relative Verschiebung
                dx = anchor.x - max(pos.x for pos in self.position_set)
                dy = anchor.y - max(pos.y for pos in self.position_set)

                # Verschiebe alle Positionen des Pieces
                translated_positions = {
                    GamePosition(pos.x + dx, pos.y + dy)
                    for pos in self.position_set
                }

                # Prüfe, ob alle verschobenen Positionen auf dem Spielbrett liegen
                if translated_positions.issubset(board):
                    yield board.difference(translated_positions), frozenset(translated_positions)

    def fits_on_board(self, board: frozenset[GamePosition]) -> bool:
        try:
            next(self.delete_from_board(board))
            return True  # Das Piece passt
        except StopIteration:
            return False  # Kein gültiger Platz gefunden


class Piece:
    def __init__(self, size: int, color: Color, form: Form):
        self.size = size
        self.color = color
        self.form = form

        assert len(self.form) == self.size, f"Das Piece mit der Farbe {self.color} ist falsch"

    def __copy__(self):
        return Piece(self.size, self.color, Form(self.form.position_set))

    def __hash__(self):
        return hash((self.size, self.color, self.form))

    def __repr__(self):
        return f"<{self.__class__.__name__} with {(self.size, self.color)}>"

    def rotate_piece(self, angle: int) -> Form:
        if angle == 0:
            return self.form
        elif angle == 90:
            return Form({GamePosition(-p.y, p.x) for p in self.form.position_set}).normalize()
        elif angle == 180:
            return Form({GamePosition(-p.x, -p.y) for p in self.form.position_set}).normalize()
        elif angle == 270:
            return Form({GamePosition(p.y, -p.x) for p in self.form.position_set}).normalize()
        else:
            raise ValueError("Angle must be 0, 90, 180, or 270")

    def delete_from_board(self, board: frozenset[GamePosition]) -> Iterator[tuple[frozenset[GamePosition], frozenset[GamePosition]]]:
        for angle in [0, 90, 180, 270]:
            for new_board, placed_piece_position in self.rotate_piece(angle).delete_from_board(board):
                yield new_board, placed_piece_position

    def fits_on_board(self, board: frozenset[GamePosition]) -> bool:
        try:
            next(self.delete_from_board(board))
            return True
        except StopIteration:
            return False

class Game:
    def __init__(self, pieces: list[Piece], board: frozenset[GamePosition], state: dict[Piece, frozenset[GamePosition]]) -> None:
        self.pieces = pieces
        self.board = board
        self.state = state

    def get_new_state(self, change: dict[Piece, frozenset[GamePosition]]) -> dict[Piece, frozenset[GamePosition]]:
        return {**change, **self.state}

    def has_already_position(self, piece: Piece) -> bool:
        return piece in self.state

    def is_valid_state(self) -> bool:
        return bool(all([piece in self.state for piece in self.pieces]))

    def sort_pieces(self) -> None:
        self.pieces = sorted(self.pieces, key=lambda piece: piece.size, reverse=True)

    def get_valid_gameboards(self) -> frozenset[frozenset[tuple[Piece, frozenset[GamePosition]]]]:
        output: set[frozenset[tuple[Piece, frozenset[GamePosition]]]] = set()
        for piece in self.pieces:
            if self.has_already_position(piece):
                continue
            for possible_new_positions, placed_piece_position in piece.delete_from_board(self.board):
                output.update(Game(self.pieces, possible_new_positions, self.get_new_state({piece: placed_piece_position})).get_valid_gameboards())
            return frozenset(output)
        assert self.is_valid_state(), self.state
        output.add(frozenset(self.state.items()))
        app = GameBoardGUI()
        app.draw_board(self.board)
        app.draw_figure(frozenset(self.state.items()))
        app.mainloop()
        return frozenset(output)

class GameBoardGUI(tk.Tk):
    def __init__(self, cell_size=40):
        super().__init__()
        self.title("Game")
        self.cell_size = cell_size

        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

    def draw_board(self, board: set[GamePosition] | frozenset[GamePosition]):
        for pos in board:
            x1 = pos.x * self.cell_size
            y1 = pos.y * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="black")

    def draw_rounded_polygon(self, points, radius=20, **kwargs):
        def get_angle(p1, p2):
            return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

        new_points = []
        for i in range(len(points)):
            p1 = points[i - 1]
            p2 = points[i]
            p3 = points[(i + 1) % len(points)]

            angle1 = get_angle(p2, p1)
            angle2 = get_angle(p2, p3)

            p1_offset = (p2[0] + radius * math.cos(angle1), p2[1] + radius * math.sin(angle1))
            p2_offset = (p2[0] + radius * math.cos(angle2), p2[1] + radius * math.sin(angle2))

            new_points.append(p1_offset)
            # Add arc here if needed
            new_points.append(p2_offset)

        self.canvas.create_line(new_points, smooth=True, **kwargs)

    def draw_figure(self, figure: frozenset[tuple[Piece, frozenset[GamePosition]]]):
        for piece, positions in figure:
            for pos in positions:
                x1 = pos.x * self.cell_size
                y1 = pos.y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=piece.color.value, outline="black")
            # self.draw_rounded_polygon([(p.x, p.y) for p in positions], radius=1, fill='', width=1)

if __name__ == "__main__":
    pieces = [
        Piece(5, Color.green, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1), GamePosition(2, 1), GamePosition(3, 1)})),
        Piece(4, Color.violet, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(3, 0)})),
        Piece(5, Color.white, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(3, 0), GamePosition(1, 1)})),
        Piece(5, Color.yellow, Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(1, 1), GamePosition(2, 1), GamePosition(2, 0)})),
        Piece(4, Color.brightGreen, Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(1, 0), GamePosition(1, 1)})),
        Piece(5, Color.red, Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(1, 0), GamePosition(1, 1), GamePosition(1, 2)})),
        Piece(5, Color.blue, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(3, 0), GamePosition(0, 1)})),
        Piece(5, Color.grey, Form({GamePosition(1, 0), GamePosition(0, 1), GamePosition(1, 1), GamePosition(2, 1), GamePosition(1, 2)})), # Star,
        Piece(5, Color.pink, Form({GamePosition(2, 0), GamePosition(2, 1), GamePosition(1, 1), GamePosition(0, 2), GamePosition(1, 2)})),
        Piece(5, Color.brightBlue, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(2, 1), GamePosition(2, 2)})),
        Piece(3, Color.white, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(0, 1)})),
        Piece(4, Color.orange, Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(1, 1), GamePosition(2, 1)})),
    ]

    gameboard = set()
    rows = 9
    columns = 9
    for x in range(columns):
        for y in range(rows):
            if (x, y) in [
                (0, 0),
                (1, 0),
                (2, 0),
                (0, 1),
                (0, 2),
                (1, 1),
                (5, 2),

                (0, 5),
                (1, 5),
                (0, 6),
                (1, 6),
                (2, 6),
                (8, 6),
                (0, 7),
                (1, 7),
                (2, 7),
                (3, 7),
                (7, 7),
                (8, 7),

                (0, 8),
                (1, 8),
                (2, 8),
                (3, 8),
                (6, 8),
                (7, 8),
                (8, 8),
            ]:
                continue
            gameboard.add(GamePosition(x, y))

    # assert len(pieces) == 12, f"Es sind keine 12 Steine: {len(pieces)}"
    # assert sum([f.size for f in pieces]) == 55, "Die Steine haben 55 Kugeln"
    assert len(gameboard) == 55, "Das Spielfeld hat 55 Plätze"
    game = Game(pieces, frozenset(gameboard), {})
    game.sort_pieces()
    valid_gameboards = game.get_valid_gameboards()
    print(valid_gameboards)
    print(len(valid_gameboards))

    # for valid_gameboard in valid_gameboards:
    #     app = GameBoardGUI()
    #     app.draw_board(gameboard)
    #     app.draw_figure(valid_gameboard)
    #     app.mainloop()


#
#     def _create_board_display(self):
#         display_frame = tk.Frame(master=self)
#         display_frame.pack(fill=tk.X)
#         self.display = tk.Label(
#             master=display_frame,
#             text="Ready?",
#             font=font.Font(size=28, weight="bold"),
#         )
#
#         self.display.pack()
#
#     def _create_board_grid(self):
#         grid_frame = tk.Frame(master=self)
#         grid_frame.pack()
#         for row in range(3):
#             self.rowconfigure(row, weight=1, minsize=50)
#             self.columnconfigure(row, weight=1, minsize=75)
#             for col in range(3):
#                 button = tk.Button(
#                     master=grid_frame,
#                     text="",
#                     font=font.Font(size=36, weight="bold"),
#                     fg="black",
#                     width=3,
#                     height=2,
#                     highlightbackground="lightblue",
#                 )
#                 self._cells[button] = (row, col)
#                 button.grid(
#                     row=row,
#                     column=col,
#                     padx=5,
#                     pady=5,
#                     sticky="nsew"
#                 )
