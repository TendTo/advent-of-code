from shared import BaseChallenge
from enum import Enum
from typing import Generator


class Step:
    def __init__(self, line: str, variant: bool = False):
        direction, steps, color = line.split()
        if not variant:
            self.direction: Direction = Direction[direction]
            self.steps: int = int(steps)
        else:
            match color[-2]:
                case "0":
                    self.direction: Direction = Direction.R
                case "1":
                    self.direction: Direction = Direction.D
                case "2":
                    self.direction: Direction = Direction.L
                case "3":
                    self.direction: Direction = Direction.U
                case _:
                    raise ValueError(f"Unknown color: {color}")

    def __repr__(self):
        return f"Step({self.direction}, {self.steps})"


class StepInterval:
    def __init__(self, point_a: tuple[int, int], point_b: tuple[int, int]):
        self.point_a = point_a
        self.point_b = point_b

    @property
    def min_x(self):
        return min(self.point_a[0], self.point_b[0])

    @property
    def max_x(self):
        return max(self.point_a[0], self.point_b[0])

    @property
    def min_y(self):
        return min(self.point_a[1], self.point_b[1])

    @property
    def max_y(self):
        return max(self.point_a[1], self.point_b[1])

    def __contains__(self, item: tuple[int, int]):
        return (
            self.min_x <= item[0] <= self.max_x and self.min_y <= item[1] <= self.max_y
        )

    def __repr__(self):
        return f"Step({self.point_a}, {self.point_b})"


class Direction(Enum):
    L = 1
    R = 2
    U = 3
    D = 4

    def __invert__(self):
        match self:
            case Direction.L:
                return Direction.R
            case Direction.R:
                return Direction.L
            case Direction.U:
                return Direction.D
            case Direction.D:
                return Direction.U
            case _:
                raise ValueError(f"Unknown direction: {self}")


class Challenge18(BaseChallenge):
    def __init__(self):
        super().__init__()
        self.steps: list[Step] = []
        self.sparse_grid: set[tuple[int, int]] = set()
        self.min_x = self.min_y = self.max_x = self.max_y = 0
        self.step_intervals: list[StepInterval] = []

    def _get_movement(self, direction: Direction) -> tuple[int, int]:
        """
        Get the movement vector for the given direction.
        """
        match direction:
            case Direction.L:
                return (-1, 0)
            case Direction.R:
                return (1, 0)
            case Direction.U:
                return (0, -1)
            case Direction.D:
                return (0, 1)
            case _:
                raise ValueError(f"Unknown direction: {direction}")

    def _inside_grid(self, x: int, y: int) -> bool:
        """
        Check if the given position is inside the grid.
        """
        if self.max_x - self.min_x == 0 or self.max_y - self.min_y == 0:
            return False
        return self.min_x <= x < self.max_x and self.min_y <= y < self.max_y

    def _get_extern(self, x: int, y: int) -> Generator[tuple[int, int], None, None]:
        for mov_x, mov_y in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_x, new_y = x + mov_x, y + mov_y
            if not self._inside_grid(new_x, new_y):
                continue
            if (new_x, new_y) in self.sparse_grid:
                continue
            yield new_x, new_y

    def _count_extern(self, x: int, y: int) -> int:
        n_extern = 0
        visited = set()
        to_visit = [(x, y)]
        while len(to_visit) > 0:
            x, y = to_visit.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            n_extern += 1
            for new_x, new_y in self._get_extern(x, y):
                if (new_x, new_y) not in visited:
                    to_visit.append((new_x, new_y))
        return n_extern

    def _populate_sparse_grid(self):
        self.sparse_grid = set()
        x, y = 0, 0
        self.min_x = self.min_y = self.max_x = self.max_y = 0
        for step in self.steps:
            mov_x, mov_y = self._get_movement(step.direction)
            for _ in range(1, step.steps + 1):
                x += mov_x
                y += mov_y
                self.sparse_grid.add((x, y))
                if x < self.min_x:
                    self.min_x = x
                if y < self.min_y:
                    self.min_y = y
                if x > self.max_x:
                    self.max_x = x
                if y > self.max_y:
                    self.max_y = y
        self.min_x -= 1
        self.min_y -= 1
        self.max_x += 2
        self.max_y += 2

    def _visualize(self):
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                if (x, y) in self.sparse_grid:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def first(self):
        """ """
        self.steps = [Step(line) for line in self.stripped_lines]
        self._populate_sparse_grid()
        self._visualize()
        return (self.max_x - self.min_x) * (
            self.max_y - self.min_y
        ) - self._count_extern(self.min_x, self.min_y)

    def _get_extern_interval(
        self, x: int, y: int
    ) -> Generator[tuple[int, int], None, None]:
        for mov_x, mov_y in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_x, new_y = x + mov_x, y + mov_y
            if not self._inside_grid(new_x, new_y):
                continue
            if any(
                (new_x, new_y) in step_interval for step_interval in self.step_intervals
            ):
                print("on interval", new_x, new_y)
                continue
            yield new_x, new_y

    def _count_extern_interval(self) -> int:
        n_extern = 0
        visited = set()
        to_visit = set()
        for x in range(self.min_x, self.max_x):
            for y in range(self.min_y, self.max_y):
                if any(
                    (x, y) in step_interval for step_interval in self.step_intervals
                ):
                    continue
                print("adding", x, y)
                to_visit.add((x, y))
        print(to_visit)
        while len(to_visit) > 0:
            x, y = to_visit.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            n_extern += 1
            for new_x, new_y in self._get_extern(x, y):
                if (new_x, new_y) not in visited:
                    to_visit.add((new_x, new_y))
        return n_extern

    def _populate_step_intervals(self):
        self.step_intervals = []
        x, y = 0, 0
        self.min_x = self.min_y = self.max_x = self.max_y = 0
        for step in self.steps:
            mov_x, mov_y = self._get_movement(step.direction)
            mov_x, mov_y = mov_x * step.steps, mov_y * step.steps
            self.step_intervals.append(StepInterval((x, y), (x + mov_x, y + mov_y)))
            x += mov_x
            y += mov_y
            if x < self.min_x:
                self.min_x = x
            if y < self.min_y:
                self.min_y = y
            if x > self.max_x:
                self.max_x = x
            if y > self.max_y:
                self.max_y = y
        self.max_x += 1
        self.max_y += 1
        print(self.step_intervals)
        print(self.min_x, self.min_y, self.max_x, self.max_y)

    def second(self):
        """ """
        self.steps = [Step(line, True) for line in self.stripped_lines]
        self._populate_step_intervals()
        return (self.max_x - self.min_x) * (
            self.max_y - self.min_y
        ) - self._count_extern_interval()


if __name__ == "__main__":
    Challenge18().run()
