from shared import BaseChallenge
from enum import Enum


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Challenge14(BaseChallenge):
    def __init__(self):
        super().__init__()
        self.grid: list[list[str]] = []

    def _inside_grid(self, x: int, y: int) -> bool:
        return 0 <= x < len(self.grid[0]) and 0 <= y < len(self.grid)

    def _count_load(self):
        total = 0
        for y, _ in enumerate(self.grid):
            for c in self.grid[y]:
                if c == "O":
                    total += len(self.grid) - y
        return total

    def _move(self, pos: tuple[int, int], direction: Direction):
        """Move the round rock (O) towards the given direction until the next position is empty (.)"""
        assert self.grid[pos[1]][pos[0]] == "O"
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
        next_x = pos[0] + movement[0]
        next_y = pos[1] + movement[1]
        while self._inside_grid(next_x, next_y) and self.grid[next_y][next_x] == ".":
            next_x += movement[0]
            next_y += movement[1]
        self.grid[pos[1]][pos[0]] = "."
        self.grid[next_y - movement[1]][next_x - movement[0]] = "O"

    def _tilt(self, direction: Direction):
        assert len(self.grid) > 0
        assert direction in (
            Direction.UP,
            Direction.DOWN,
            Direction.LEFT,
            Direction.RIGHT,
        )

        if direction == Direction.UP:
            for y, _ in enumerate(self.grid):
                for x, _ in enumerate(self.grid[y]):
                    if self.grid[y][x] == "O":
                        self._move((x, y), direction)
        elif direction == Direction.DOWN:
            for y in range(len(self.grid) - 1, -1, -1):
                for x, _ in enumerate(self.grid[y]):
                    if self.grid[y][x] == "O":
                        self._move((x, y), direction)
        elif direction == Direction.LEFT:
            for x, _ in enumerate(self.grid[0]):
                for y, _ in enumerate(self.grid):
                    if self.grid[y][x] == "O":
                        self._move((x, y), direction)
        elif direction == Direction.RIGHT:
            for x in range(len(self.grid[0]) - 1, -1, -1):
                for y, _ in enumerate(self.grid):
                    if self.grid[y][x] == "O":
                        self._move((x, y), direction)

    def first(self):
        """
        --- Day 14: Parabolic Reflector Dish ---
        You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.

        The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

        This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

        Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

        In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

        O....#....
        O.OO#....#
        .....##...
        OO.#O....O
        .O.....O#.
        O.#..O.#.#
        ..O..#O..O
        .......O..
        #....###..
        #OO..#....
        Start by tilting the lever so all of the rocks will slide north as far as they will go:

        OOOO.#.O..
        OO..#....#
        OO..O##..O
        O..#.OO...
        ........#.
        ..#....#.#
        ..O..#.O.O
        ..O.......
        #....###..
        #....#....
        You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

        The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

        OOOO.#.O.. 10
        OO..#....#  9
        OO..O##..O  8
        O..#.OO...  7
        ........#.  6
        ..#....#.#  5
        ..O..#.O.O  4
        ..O.......  3
        #....###..  2
        #....#....  1
        The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

        Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?
        """
        self.grid = list(map(list, self.stripped_lines))
        self._tilt(Direction.UP)
        return self._count_load()

    def _cycle(self):
        self._tilt(Direction.UP)
        self._tilt(Direction.LEFT)
        self._tilt(Direction.DOWN)
        self._tilt(Direction.RIGHT)

    def _get_grid_hash(self) -> int:
        """Collect all the coordinates of the round rocks (O) to be able to
        recognize when the same configuration is reached again.
        """
        return hash(
            tuple(
                (x, y)
                for y, line in enumerate(self.grid)
                for x, c in enumerate(line)
                if c == "O"
            )
        )

    def second(self):
        """
        --- Part Two ---
        The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to do just that!

        Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

        Here's what happens in the example above after each of the first few cycles:

        After 1 cycle:
        .....#....
        ....#...O#
        ...OO##...
        .OO#......
        .....OOO#.
        .O#...O#.#
        ....O#....
        ......OOOO
        #...O###..
        #..OO#....

        After 2 cycles:
        .....#....
        ....#...O#
        .....##...
        ..O#......
        .....OOO#.
        .O#...O#.#
        ....O#...O
        .......OOO
        #..OO###..
        #.OOO#...O

        After 3 cycles:
        .....#....
        ....#...O#
        .....##...
        ..O#......
        .....OOO#.
        .O#...O#.#
        ....O#...O
        .......OOO
        #...O###.O
        #.OOO#...O
        This process should work if you leave it running long enough, but you're still worried about the north support beams. To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 1000000000 cycles.

        In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

        Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?
        """
        SPINS = 1000000000
        self.grid = list(map(list, self.stripped_lines))
        hashes_timestamps = {}  # first iteration when a certain grid was encountered
        hashes = set()  # set of hashes of the grid encountered so far
        hashes.add(self._get_grid_hash())
        hashes_timestamps[next(iter(hashes))] = 0
        i = 0
        while i < SPINS:
            self._cycle()
            grid_hash = self._get_grid_hash()
            if grid_hash in hashes:  # a loop has been detected
                cycle_length = i + 1 - hashes_timestamps[grid_hash]
                # skip to the last iteration of the loop
                i = SPINS - ((SPINS - hashes_timestamps[grid_hash]) % cycle_length)
                break
            hashes.add(grid_hash)
            hashes_timestamps[grid_hash] = len(hashes_timestamps)
            i += 1

        # complete the remaining iterations
        while i < SPINS:
            self._cycle()
            i += 1
        return self._count_load()


if __name__ == "__main__":
    Challenge14().run()
