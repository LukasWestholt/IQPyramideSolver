from pyramide.Game import Game
from pyramide.Color import Color
from pyramide.Form import Form
from pyramide.GameBoard import GameBoard
from pyramide.GameBoardGUI import GameBoardGUI
from pyramide.GamePosition import GamePosition
from pyramide.Piece import Piece

if __name__ == "__main__":
    pieces = [
        Piece(Color.green, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1), GamePosition(2, 1), GamePosition(3, 1)})),
        Piece(Color.violet, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(3, 0)})),
        Piece(Color.white, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(3, 0), GamePosition(1, 1)})),
        Piece(Color.yellow, Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(1, 1), GamePosition(2, 1), GamePosition(2, 0)})),
        Piece(Color.brightGreen, Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(1, 0), GamePosition(1, 1)})),
        Piece(Color.red, Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(1, 0), GamePosition(1, 1), GamePosition(1, 2)})),
        Piece(Color.blue, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(3, 0), GamePosition(0, 1)})),
        Piece(Color.grey, Form({GamePosition(1, 0), GamePosition(0, 1), GamePosition(1, 1), GamePosition(2, 1), GamePosition(1, 2)})), # Star,
        Piece(Color.pink, Form({GamePosition(2, 0), GamePosition(2, 1), GamePosition(1, 1), GamePosition(0, 2), GamePosition(1, 2)})),
        Piece(Color.brightBlue, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(2, 1), GamePosition(2, 2)})),
        Piece(Color.white, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(0, 1)})),
        Piece(Color.orange, Form({GamePosition(0, 0), GamePosition(0, 1), GamePosition(1, 1), GamePosition(2, 1)})),
    ]
    gameboardSet = set()
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
            gameboardSet.add(GamePosition(x, y))

    gameboard = GameBoard(gameboardSet)

    assert len(pieces) == 12, f"Es sind keine 12 Steine: {len(pieces)}"
    assert sum([f.size for f in pieces]) == 55, f"Die Steine haben keine 55 Kugeln: {sum([f.size for f in pieces])}"
    assert len(gameboard) == 55, f"Das Spielfeld hat keine 55 Plätze: {len(gameboard)}"

    piece1 = Piece(Color.white, Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(2, 0), GamePosition(3, 0), GamePosition(1, 1)}))
    pieces.remove(piece1)
    piece2 = Piece(Color.pink, Form({GamePosition(2, 0), GamePosition(2, 1), GamePosition(1, 1), GamePosition(0, 2), GamePosition(1, 2)}))
    pieces.remove(piece2)
    new = {
        x for x in gameboard.position_set
            if x not in (
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
    gameboardNew = GameBoard({GamePosition(p.x, -p.y) for p in gameboardNew.position_set}).normalize_to_gameboard()

    game = Game(pieces, gameboardNew, {})
    game.sort_pieces()
    valid_gameboards = game.get_valid_gameboards(parallel=True)

    for valid_gameboard in valid_gameboards:
        print(valid_gameboard)
        app = GameBoardGUI()
        app.draw_board(gameboard)
        app.draw_figure(valid_gameboard)
        app.mainloop()
