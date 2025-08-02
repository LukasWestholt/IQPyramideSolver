from collections import deque

from pyramide.game_position import GamePosition


class GameBoard:
    def __init__(
        self, position_set: set[GamePosition] | frozenset[GamePosition]
    ) -> None:
        self.position_set = frozenset(position_set)

    def __len__(self) -> int:
        return len(self.position_set)

    def __hash__(self) -> int:
        return hash((self.position_set,))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, GameBoard):
            return self.position_set == other.position_set
        return False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} with {set(self.position_set)}>"

    def __str__(self) -> str:
        if not self.position_set:
            return "<empty form>"

        min_x = min(p.x for p in self.position_set)
        max_x = max(p.x for p in self.position_set)
        min_y = min(p.y for p in self.position_set)
        max_y = max(p.y for p in self.position_set)

        rows = []
        rows.append("-" * (max_x - min_x + 1))
        for y in range(max_y, min_y - 1, -1):
            row = ""
            for x in range(min_x, max_x + 1):
                if GamePosition(x, y) in self.position_set:
                    row += "#"
                else:
                    row += "."
            rows.append(row)
        rows.append("-" * (max_x - min_x + 1))
        return "\n".join(rows)

    def get_neighbors(self, position: GamePosition) -> set[GamePosition]:
        neighbors = set()
        # Check 4-directional neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = GamePosition(position.x + dx, position.y + dy)
            if neighbor in self.position_set:
                neighbors.add(neighbor)
        return neighbors

    def assert_all_positions_connected(self) -> None:
        if not self.position_set:
            return

        visited: set[GamePosition] = set()
        queue = deque([set(self.position_set).pop()])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    queue.append(neighbor)

        assert len(visited) == len(self.position_set), (
            f"{self.position_set} has a Problem: {self.position_set.symmetric_difference(visited)}"
        )
        return

    def normalize_to_gameboard(self) -> "GameBoard":
        min_x = min(p.x for p in self.position_set)
        min_y = min(p.y for p in self.position_set)
        return GameBoard(
            {GamePosition(p.x - min_x, p.y - min_y) for p in self.position_set}
        )

    def has_min_connected_gamepositions(self, min_connected_gamepositions: int) -> bool:
        visited = set()

        for pos in self.position_set:
            if pos in visited:
                continue

            # Start BFS from this position
            queue = deque([pos])
            component = set()

            while queue:
                current = queue.popleft()
                if current in component:
                    continue
                component.add(current)

                for neighbor in self.get_neighbors(current):
                    if neighbor not in component:
                        queue.append(neighbor)

            # Mark all positions in this component as visited
            visited.update(component)

            # Check if the component is large enough
            if len(component) < min_connected_gamepositions:
                return False
        return True
