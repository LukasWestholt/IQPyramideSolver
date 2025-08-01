from pyramide.Game import Game
from pyramide.Color import Color
from pyramide.Form import Form
from pyramide.GameBoard import GameBoard
from pyramide.GameBoardGUI import GameBoardGUI
from pyramide.GamePosition import GamePosition
from pyramide.Piece import Piece
from scripts.iq_pyramide_helpers import get_pieces, get_gameboard

if __name__ == "__main__":
    pieces = get_pieces()
    gameboard = get_gameboard()

    piece1 = Piece(Color.white, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(0, 1)})).mirror_piece("x")
    pieces.remove(piece1)
    piece2 = Piece(Color.orange, Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(1, 1), GamePosition(2, 1)})).mirror_piece("x")
    pieces.remove(piece2)
    new = {
        x for x in gameboard.position_set
            if x not in (
            GamePosition(x=8, y=0),
            GamePosition(x=8, y=1),
            GamePosition(x=7, y=1),

            GamePosition(x=8, y=2),
            GamePosition(x=7, y=2),
            GamePosition(x=6, y=2),
            GamePosition(x=6, y=1),
        )
    }
    assert len(new) == (len(gameboard) - 7)
    gameboardNew = GameBoard(new)

    game = Game(pieces, gameboardNew, {})
    game.sort_pieces()
    valid_gameboards = game.get_valid_gameboards(parallel=True)

    for valid_gameboard in valid_gameboards:
        print(valid_gameboard)
        app = GameBoardGUI()
        app.draw_board(gameboard)
        app.draw_figure(valid_gameboard)
        app.mainloop()
