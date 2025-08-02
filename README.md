# IQPyramideSolver 🧩

Solves the **IQ pyramid logic puzzle**: given figures at specific positions,
determine the triangular arrangement under certain rules.

---

## Table of Contents

* [Installation & Setup](#installation--setup)
* [Usage](#usage)
* [Algorithm](#algorithm)
* [Game Description](#game-description)
* [Example](#example)

---

## Installation & Setup

1. **Clone the repo**

   ```
   git clone https://github.com/LukasWestholt/IQPyramideSolver.git
   cd IQPyramideSolver
   ```

2. **Install dependencies using Poetry**
   Ensure you have Poetry installed. Then run:

   ```
   poetry install
   ```

3. **Create `game.py`**
   The script requires a file called `game.py` in the project directory `scripts/`.
It should define your puzzle input, see `game1.py`, `game2.py` or `game3.py`

## ✅ Running Tests

Unit tests are provided to verify the functionality.

To run the tests:

```bash
poetry run python -m unittest discover tests
```

---

## Usage

Once set up:

```
poetry run python -m scripts.game
```

* The script will read `game.py`, interpret the given clues, and compute all valid pyramid solutions.
* Outputs are shown via tkinter as possible completed pyramids, one by one.

---

<!---
## Algorithm

The solver implements a **constraint-based backtracking search**:

* **Propagation**: For each missing cell, maintain a set of possible values based on remaining numbers.
* **Constraint**: Adjacent sums must follow the puzzle rule (e.g. sum of two cells equals value below).
* **Heuristic ordering**: Picks the next cell with the fewest possibilities to speed up the search.
* **Backtracking**: Assign a possible value, propagate constraints recursively; backtrack on conflict.

This efficiently prunes large swathes of the search space and finds all unique solutions.
-->

### 🚀 Features

- **GamePosition**: Represents a coordinate on the board.
- **Form**:
  - Represents the shape of a piece using a set of connected `GamePosition`s.
  - Validates connectivity.
  - Supports placement logic.
- **Piece**:
  - Represents a puzzle piece with a color and form.
  - Supports rotation (0°, 90°, 180°, 270°).
  - Supports mirroring (horizontal and vertical).
  - Checks if a piece fits on the board.
  - Can remove itself from the board.


###  🛠️ Usage

To use the game logic, define pieces and a game board using the provided classes. You can check if a piece fits on the board and manipulate its orientation.

```python
form = Form({GamePosition(0, 0), GamePosition(1, 0), GamePosition(1, 1)})
piece = Piece(Color.green, form)

board = {
    GamePosition(2, 2),
    GamePosition(3, 2),
    GamePosition(3, 3),
}

if piece.fits_on_board(board):
    print("Piece fits!")
```

---

## Game Description

The "IQ Pyramid" puzzle consists of a grid-based board and a set of uniquely
shaped pieces.
Each piece is defined by its color and form (a set of connected balls).
The game logic ensures that pieces are valid, connected, and can be placed on the board in various orientations.

EAN: 4260071878168
### German Description
IQ Pyramide

Fördern Sie Intelligenz, logisches Denken, räumliche Vorstellungskraft und Konzentrationsfähigkeit! 12 unterschiedlich geformte Teile müssen immer neu kombiniert werden - in 2D und 3D. Inkl. Heft mit 66 Aufgaben von sehr einfach bis extrem schwierig und Lösungen!

Anleitung: https://gesellschaftsspiele.spielen.de/uploads/files/1532/54ef68548153e.pdf

---

## 🤝 Contributing & License

Contributions are welcome! Feel free to open issues or submit pull requests.

### Guidelines

Use `pre-commit` by execute

```
pre-commit install
```

## 📄 License

This project is released under the **MIT License** (see `LICENSE`).

---

Enjoy solving IQ pyramids!
