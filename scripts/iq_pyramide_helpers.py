from pyramide.Color import Color
from pyramide.Form import Form
from pyramide.GameBoard import GameBoard
from pyramide.GamePosition import GamePosition
from pyramide.Piece import Piece

def get_pieces():
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
    assert len(pieces) == 12, f"Es sind keine 12 Steine: {len(pieces)}"
    assert sum([len(f) for f in pieces]) == 55, f"Die Steine haben keine 55 Kugeln: {sum([len(f) for f in pieces])}"

    return [piece.mirror_piece("x") for piece in pieces] # hotfix for (0,0) top left

def get_gameboard():
    gameboard_set = set()
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
            gameboard_set.add(GamePosition(x, y))

    assert len(GameBoard(gameboard_set)) == 55, f"Das Spielfeld hat keine 55 Plätze: {len(GameBoard(gameboard_set))}"
    return GameBoard(gameboard_set)
