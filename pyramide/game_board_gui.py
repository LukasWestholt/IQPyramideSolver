import math
import tkinter as tk
from typing import Any

from pyramide.game_board import GameBoard
from pyramide.solved_game import SolvedGame


class GameBoardGUI(tk.Tk):
    def __init__(self, cell_size: int = 40) -> None:
        super().__init__()
        self.title("Game")
        self.cell_size = cell_size

        self.canvas = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas.pack()

    def draw_board(self, board: GameBoard) -> None:
        for pos in board.position_set:
            x1 = pos.x * self.cell_size
            y1 = pos.y * self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="black")

    def draw_rounded_polygon(
        self,
        points: list[tuple[int, int]],
        radius: int = 20,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        def get_angle(p1: tuple[int, int], p2: tuple[int, int]) -> float:
            return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

        new_points = []
        for i in range(len(points)):
            p1 = points[i - 1]
            p2 = points[i]
            p3 = points[(i + 1) % len(points)]

            angle1 = get_angle(p2, p1)
            angle2 = get_angle(p2, p3)

            p1_offset = (
                p2[0] + radius * math.cos(angle1),
                p2[1] + radius * math.sin(angle1),
            )
            p2_offset = (
                p2[0] + radius * math.cos(angle2),
                p2[1] + radius * math.sin(angle2),
            )

            new_points.append(p1_offset)
            # Add arc here if needed
            new_points.append(p2_offset)

        self.canvas.create_line(new_points, smooth=True, **kwargs)

    def draw_figure(self, figure: SolvedGame) -> None:
        for piece, positions in figure.gameboard:
            for pos in positions:
                x1 = pos.x * self.cell_size
                y1 = pos.y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=piece.color.value, outline="black"
                )
            # self.draw_rounded_polygon([(p.x, p.y) for p in positions], radius=1, fill='', width=1)


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
