from shared import BaseChallenge
from enum import Enum
from dataclasses import dataclass
from typing import Generator


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def __invert__(self):
        match self:
            case Direction.LEFT:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.LEFT
            case Direction.UP:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.UP
            case _:
                raise ValueError(f"Unknown direction: {self}")


@dataclass
class DistanceNode:
    distance: int
    step: "Step"

    def __lt__(self, other: "DistanceNode"):
        return self.distance < other.distance

    def __eq__(self, other: "DistanceNode"):
        return self.distance == other.distance

    def __hash__(self):
        return hash((self.distance, self.step))

    def __repr__(self):
        return f"DistanceNode({self.distance})"


@dataclass
class Step:
    pos: tuple[int, int]
    direction: Direction
    steps_straight: int

    @property
    def x(self) -> int:
        return self.pos[0]

    @property
    def y(self) -> int:
        return self.pos[1]

    def __hash__(self):
        return hash((self.pos, self.direction, self.steps_straight))

    def __eq__(self, other):
        return (
            self.pos == other.pos
            and self.direction == other.direction
            and self.steps_straight == other.steps_straight
        )

    def __repr__(self):
        return f"Step({self.pos}, {self.direction}, {self.steps_straight})"


class Challenge17(BaseChallenge):
    def __init__(self):
        super().__init__()
        self.grid: tuple[tuple[int]] = []
        self.end: tuple[int, int] = (0, 0)

    def _get_movement(self, direction: Direction) -> tuple[int, int]:
        """
        Get the movement vector for the given direction.
        """
        match direction:
            case Direction.LEFT:
                movement = (-1, 0)
            case Direction.RIGHT:
                movement = (1, 0)
            case Direction.UP:
                movement = (0, -1)
            case Direction.DOWN:
                movement = (0, 1)
            case _:
                raise ValueError(f"Unknown direction: {direction}")
        return movement

    def _inside_grid(self, x: int, y: int) -> bool:
        """
        Check if the given position is inside the grid.
        """
        if len(self.grid) == 0:
            return False
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)

    def _get_neighbors_crucible(self, step: Step) -> Generator[Step, None, None]:
        for new_direction in (
            Direction.LEFT,
            Direction.RIGHT,
            Direction.UP,
            Direction.DOWN,
        ):
            if step.steps_straight == 2 and new_direction == step.direction:
                continue
            if step.direction == ~new_direction:
                continue
            mov_x, mov_y = self._get_movement(new_direction)
            new_x, new_y = step.x + mov_x, step.y + mov_y
            if not self._inside_grid(new_x, new_y):
                continue
            yield Step(
                (new_x, new_y),
                new_direction,
                step.steps_straight + 1 if new_direction == step.direction else 0,
            )

    def _dijkstra(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> int:
        """
        Compute the minimum distance between the given start and end positions.
        """
        right_step = Step((start[0] + 1, start[1]), Direction.RIGHT, 0)
        down_step = Step((start[0], start[1] + 1), Direction.DOWN, 0)
        distances = {
            right_step: self.grid[right_step.y][right_step.x],
            down_step: self.grid[down_step.y][down_step.x],
        }
        visited = set()
        to_visit = set((right_step, down_step))
        while len(to_visit) > 0:
            current = min(to_visit, key=lambda step: distances[step])
            to_visit.remove(current)
            visited.add(current)
            for step in self._get_neighbors_crucible(current):
                if step in visited:
                    continue
                new_cost = distances[current] + self.grid[step.y][step.x]
                if step not in distances or new_cost < distances[step]:
                    distances[step] = new_cost
                    to_visit.add(step)
        return min(dist for step, dist in distances.items() if step.pos == end)

    def first(self):
        """ """
        self.grid = tuple(
            tuple(map(int, (n for n in line))) for line in self.stripped_lines
        )
        self.end = (len(self.grid[0]) - 1, len(self.grid) - 1)
        return self._dijkstra((0, 0), self.end)

    def _get_neighbors_ultracrucible(self, step: Step) -> Generator[Step, None, None]:
        if step.steps_straight < 3:
            mov_x, mov_y = self._get_movement(step.direction)
            new_x, new_y = step.x + mov_x, step.y + mov_y
            if not self._inside_grid(new_x, new_y):
                return
            yield Step((new_x, new_y), step.direction, step.steps_straight + 1)
            return
        for new_direction in (
            Direction.LEFT,
            Direction.RIGHT,
            Direction.UP,
            Direction.DOWN,
        ):
            if step.steps_straight == 9 and new_direction == step.direction:
                continue
            if step.direction == ~new_direction:
                continue
            mov_x, mov_y = self._get_movement(new_direction)
            new_x, new_y = step.x + mov_x, step.y + mov_y
            if not self._inside_grid(new_x, new_y):
                continue
            yield Step(
                (new_x, new_y),
                new_direction,
                step.steps_straight + 1 if new_direction == step.direction else 0,
            )

    def _ultra_dijkstra(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
    ) -> int:
        """
        Compute the minimum distance between the given start and end positions.
        """
        right_step = Step((start[0] + 1, start[1]), Direction.RIGHT, 0)
        down_step = Step((start[0], start[1] + 1), Direction.DOWN, 0)
        distances = {
            right_step: self.grid[right_step.y][right_step.x],
            down_step: self.grid[down_step.y][down_step.x],
        }
        visited = set()
        to_visit = set((right_step, down_step))
        while len(to_visit) > 0:
            current = min(to_visit, key=lambda step: distances[step])
            to_visit.remove(current)
            if current in visited:
                continue
            visited.add(current)
            for step in self._get_neighbors_ultracrucible(current):
                if step in visited:
                    continue
                new_cost = distances[current] + self.grid[step.y][step.x]
                if step not in distances or new_cost < distances[step]:
                    distances[step] = new_cost
                    if step.pos != end:
                        to_visit.add(step)
        return min(
            dist
            for step, dist in distances.items()
            if step.pos == end and step.steps_straight >= 3
        )

    def second(self):
        """ """
        self.grid = tuple(
            tuple(map(int, (n for n in line))) for line in self.stripped_lines
        )
        self.end = (len(self.grid[0]) - 1, len(self.grid) - 1)
        return self._ultra_dijkstra((0, 0), self.end)


if __name__ == "__main__":
    Challenge17().run()
