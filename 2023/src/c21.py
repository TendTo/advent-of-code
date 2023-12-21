from shared import BaseChallenge
from typing import Generator


class Challenge21(BaseChallenge):
    def __init__(self, steps: int = 64):
        super().__init__()
        self.steps = steps
        self.grid: tuple[str] = []
        self.start: tuple[int, int] = (0, 0)

    def _inside_grid(self, x: int, y: int) -> bool:
        """
        Check if the given position is inside the grid.
        """
        if len(self.grid) == 0:
            return False
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)

    def _get_neighbors(self, x: int, y: int) -> Generator[tuple[int, int], None, None]:
        for movement in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            mov_x, mov_y = movement
            new_x, new_y = x + mov_x, y + mov_y
            if not self._inside_grid(new_x, new_y):
                continue
            if self.grid[new_y][new_x] == "#":
                continue
            yield (new_x, new_y)

    def _bfs(self, start: tuple[int, int]) -> int:
        """
        Compute the minimum distance between the given start and end positions.
        """
        odd_visited: set[tuple[int, int]] = set()
        even_visited: set[tuple[int, int]] = set()
        to_visit = [(start, 0)]
        while len(to_visit) > 0:
            current, timestamp = to_visit.pop(0)
            if current in odd_visited or current in even_visited:
                continue
            if timestamp & 1:
                even_visited.add(current)
            else:
                odd_visited.add(current)
            if timestamp >= self.steps:
                continue
            for new_node in self._get_neighbors(current[0], current[1]):
                to_visit.append((new_node, timestamp + 1))
        return len(even_visited) if self.steps & 1 == 0 else len(odd_visited)

    def _find_start(self) -> tuple[int, int]:
        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if char == "S":
                    self.start = (x, y)
                    return (x, y)
        raise ValueError("No start found")

    def first(self):
        """ """
        self.grid = tuple(self.stripped_lines)
        start = self._find_start()
        return self._bfs(start)

    def second(self):
        """ """
        self.grid = tuple(self.stripped_lines)
        start = self._find_start()


if __name__ == "__main__":
    Challenge21().run()
