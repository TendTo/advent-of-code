from shared import BaseChallenge
from typing import Generator, Iterable


class Challenge23(BaseChallenge):
    def __init__(self, steps: int = 64):
        super().__init__()
        self.steps = steps
        self.grid: tuple[str] = []
        self.start: tuple[int, int] = (0, 0)
        self.visited: dict[tuple[int, int], bool] = {}
        self.distances: dict[tuple[int, int], int] = {}
        self.prev_start: tuple[int, int] = (-1, -1)
        self.edges: dict[tuple[int, int], dict[tuple[int, int], int]] = {}

    def _inside_grid(self, x: int, y: int) -> bool:
        """
        Check if the given position is inside the grid.
        """
        if len(self.grid) == 0:
            return False
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)

    def _get_directions(self, x: int, y: int) -> Iterable[tuple[int, int]]:
        if self.grid[y][x] in (".", "S"):
            return (-1, 0), (1, 0), (0, -1), (0, 1)
        if self.grid[y][x] == ">":
            return ((1, 0),)
        if self.grid[y][x] == "<":
            return ((-1, 0),)
        if self.grid[y][x] == "^":
            return ((0, -1),)
        if self.grid[y][x] == "v":
            return ((0, 1),)
        raise ValueError(f"Unknown direction: {self.grid[y][x]}")

    def _get_neighbors_dag(
        self, x: int, y: int, previous_pos: tuple[int, int] = None
    ) -> Generator[tuple[int, int], None, None]:
        for movement in self._get_directions(x, y):
            mov_x, mov_y = movement
            new_x, new_y = x + mov_x, y + mov_y
            if not self._inside_grid(new_x, new_y):
                continue
            if self.grid[new_y][new_x] == "#":
                continue
            if previous_pos is not None and (new_x, new_y) == previous_pos:
                continue
            yield (new_x, new_y)

    def _bfs_exp(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        """
        Compute the maximum distance between the given start and end positions.
        """
        previous: dict[tuple[int, int], tuple[int, int] | None] = {}
        children: dict[tuple[int, int], set[tuple[int, int]]] = {}
        visited: set[tuple[int, int]] = set()
        previous[start] = None
        to_visit = [(start, 0)]
        while len(to_visit) > 0:
            current, timestamp = to_visit.pop(0)
            if current in visited:
                continue
            visited.add(current)
            for new_node in self._get_neighbors_dag(current[0], current[1]):
                children.setdefault(current, set()).add(new_node)
                previous[new_node] = current
                to_visit.insert(0, (new_node, timestamp + 1))

    def _bfs_dag(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        """
        Compute the maximum distance between the given start and end positions.
        """
        visited: set[tuple[int, int]] = set()
        distances: dict[tuple[int, int], int] = {}
        to_visit = [(start, None)]
        distances[start] = 0
        while len(to_visit) > 0:
            current, prev = to_visit.pop(0)
            if current in visited:
                continue
            visited.add(current)
            for new_node in self._get_neighbors_dag(current[0], current[1], prev):
                to_visit.append((new_node, current))
                new_distance = distances[current] + 1
                if new_node not in distances:
                    distances[new_node] = new_distance
                elif new_distance > distances[new_node]:
                    distances[new_node] = new_distance
                    if new_node in visited:
                        visited.remove(new_node)
        return distances[end]

    def _find_start(self) -> tuple[int, int]:
        assert len(self.grid) > 0
        for x, char in enumerate(self.grid[0]):
            if char == ".":
                return (x, 0)
        raise ValueError("No start found")

    def _find_end(self) -> tuple[int, int]:
        assert len(self.grid) > 0
        for x, char in enumerate(self.grid[-1]):
            if char == ".":
                return (x, len(self.grid) - 1)
        raise ValueError("No end found")

    def first(self):
        """ """
        self.grid = tuple(self.stripped_lines)
        start = self._find_start()
        end = self._find_end()
        return self._bfs_dag(start, end)

    def _get_neighbors(
        self, x: int, y: int, prev: tuple[int, int] = None
    ) -> Generator[tuple[int, int], None, None]:
        for movement in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            mov_x, mov_y = movement
            new_x, new_y = x + mov_x, y + mov_y
            if not self._inside_grid(new_x, new_y):
                continue
            if self.grid[new_y][new_x] == "#":
                continue
            if prev is not None and (new_x, new_y) == prev:
                continue
            if self.visited.get((new_x, new_y), False):
                continue
            if self.prev_start == (new_x, new_y):
                continue
            yield (new_x, new_y)

    def _dfs(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        """
        Compute the maximum distance between the given start and end positions.
        """
        stack: list[tuple[tuple[int, int], int]] = [(start, 0)]

        while len(stack) > 0:
            current, current_dist = stack[0]
            if current in self.visited and self.visited[current]:
                self.visited[current] = False
                stack.pop(0)
                continue

            self.visited[current] = True
            if self.distances.get(current, 0) < current_dist:
                self.distances[current] = current_dist

            if current == end:
                continue

            for new_node in self._get_neighbors(current[0], current[1]):
                if not self.visited.get(new_node, False):
                    stack.insert(0, (new_node, current_dist + 1))

    def _dfs_interceptions(self, start: tuple[int, int], end: tuple[int, int]) -> int:
        """
        Compute the maximum distance between the given start and end positions.
        """
        stack: list[tuple[tuple[int, int], int]] = [(start, 0)]

        while len(stack) > 0:
            current, current_dist = stack[0]
            if current in self.visited and self.visited[current]:
                self.visited[current] = False
                stack.pop(0)
                continue

            self.visited[current] = True
            if self.distances.get(current, 0) < current_dist:
                self.distances[current] = current_dist

            if current == end:
                continue

            for new_node, distance in self.edges[current].items():
                if not self.visited.get(new_node, False):
                    stack.insert(0, (new_node, current_dist + distance))

    def _find_start_interceptions(self) -> tuple[tuple[int, int], tuple[int, int], int]:
        distance = 0
        current = self._find_start()
        prev = None
        while True:
            neighbors = list(self._get_neighbors(current[0], current[1], prev))
            if len(neighbors) == 1:
                prev = current
                current = neighbors[0]
                distance += 1
            else:
                break
        return current, prev, distance

    def _find_end_interceptions(self) -> tuple[tuple[int, int], tuple[int, int], int]:
        distance = 0
        current = self._find_end()
        prev = None
        while True:
            neighbors = list(self._get_neighbors(current[0], current[1], prev))
            if len(neighbors) == 1:
                distance += 1
                prev = current
                current = neighbors[0]
            else:
                break
        return current, prev, distance

    def _find_interceptions(self) -> set[tuple[int, int]]:
        interceptions: set[tuple[int, int]] = set()
        for y, line in enumerate(self.grid):
            for x, c in enumerate(line):
                if c == "#":
                    continue
                if sum(1 for _ in self._get_neighbors(x, y)) > 2:
                    interceptions.add((x, y))
        return interceptions

    def _compute_edges(
        self, start: tuple[int, int], intersections: set[tuple[int, int]]
    ):
        visited: set[tuple[int, int]] = set()
        to_visit: list[tuple[tuple[int, int], tuple[int, int], int]] = [
            (start, None, 0)
        ]
        while len(to_visit) > 0:
            current, prev, distance = to_visit.pop()
            if current in visited:
                continue
            visited.add(current)
            for n in self._get_neighbors(current[0], current[1], prev):
                if n in intersections:
                    self.edges.setdefault(start, {})[n] = distance + 1
                else:
                    to_visit.append((n, current, distance + 1))

    def _visualize(self):
        for y, line in enumerate(self.grid):
            for x, char in enumerate(line):
                if self.visited.get((x, y), False):
                    print("x", end="")
                else:
                    print(char, end="")
            print()

    def second(self):
        """ """
        self.grid = tuple(self.stripped_lines)
        interceptions = self._find_interceptions()
        start, self.prev_start, start_dist = self._find_start_interceptions()
        end, _, end_dist = self._find_end_interceptions()
        self.edges = {}
        for interception in interceptions:
            self._compute_edges(interception, interceptions)
        self._dfs_interceptions(start, end)
        return start_dist + end_dist + self.distances[end]


if __name__ == "__main__":
    Challenge23().run()
