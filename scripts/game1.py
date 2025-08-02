from pyramide.Color import Color
from pyramide.Form import Form
from pyramide.Game import Game
from pyramide.GameBoard import GameBoard
from pyramide.GameBoardGUI import GameBoardGUI
from pyramide.GamePosition import GamePosition
from pyramide.Piece import Piece
from scripts.iq_pyramide_helpers import get_gameboard, get_pieces

if __name__ == "__main__":
    pieces = get_pieces()
    gameboard = get_gameboard()

    piece1 = Piece(
        Color.white,
        Form(
            {
                GamePosition(0, 0),
                GamePosition(1, 0),
                GamePosition(2, 0),
                GamePosition(3, 0),
                GamePosition(1, 1),
            }
        ),
    )
    pieces.remove(piece1)
    piece2 = Piece(
        Color.pink,
        Form(
            {
                GamePosition(2, 0),
                GamePosition(2, 1),
                GamePosition(1, 1),
                GamePosition(0, 2),
                GamePosition(1, 2),
            }
        ),
    )
    pieces.remove(piece2)
    new = {
        x
        for x in gameboard.position_set
        if x
        not in (
            GamePosition(x=8, y=0),
            GamePosition(x=8, y=1),
            GamePosition(x=8, y=2),
            GamePosition(x=8, y=3),
            GamePosition(x=7, y=1),
            GamePosition(x=6, y=1),
            GamePosition(x=5, y=1),
            GamePosition(x=7, y=2),
            GamePosition(x=6, y=2),
            GamePosition(x=7, y=3),
        )
    }
    assert len(new) == (len(gameboard) - 10)
    gameboardNew = GameBoard(new)

    game = Game(pieces, gameboardNew, {})
    game.sort_pieces()
    valid_gameboards = game.solve(parallel=True)

    unique_valid_gameboards = set()

    for valid_gameboard in valid_gameboards:
        if valid_gameboard not in unique_valid_gameboards:
            print(valid_gameboard)
            app = GameBoardGUI()
            app.draw_board(gameboardNew)
            app.draw_figure(valid_gameboard)
            app.mainloop()
            unique_valid_gameboards.add(valid_gameboard)

    print(len(unique_valid_gameboards))

    assert len(unique_valid_gameboards) == 7, "Nicht alle Ergebnisse gefunden!!"
