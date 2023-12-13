from shared import BaseChallenge


class Challenge11(BaseChallenge):
    def __init__(self, multiplier: int = 1000):
        super().__init__()
        self.grid: tuple[str] = []
        self.expanded_grid: list[list[str]] = []
        self.visited = set()
        self.y_offsets: list[int] = []
        self.x_offsets: list[int] = []
        self.multiplier = multiplier

    def _expand_grid_dense(self):
        # expand rows
        self.expanded_grid = []
        for row in self.grid:
            if all(char == "." for char in row):
                self.expanded_grid.append(list(row))
                self.expanded_grid.append(list(row))
            else:
                self.expanded_grid.append(list(row))
        for i in range(len(self.grid[0]) - 1, -1, -1):
            if all(row[i] == "." for row in self.grid):
                for row in self.expanded_grid:
                    row.insert(i, ".")

    def _starts_dense(self):
        for y, row in enumerate(self.expanded_grid):
            for x, char in enumerate(row):
                if char == "#":
                    yield x, y

    def _bfs_dense(self, start: tuple[int, int]) -> list[tuple[int, int], int]:
        sx, sy = start
        distances: list[tuple[int, int], int] = []
        for y, row in enumerate(self.expanded_grid):
            for x, char in enumerate(row):
                if char == "#" and (x, y) not in self.visited:
                    distances.append(((x, y), abs(x - sx) + abs(y - sy)))
        return distances

    def first(self):
        """
        --- Day 11: Cosmic Expansion ---
        You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

        He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

        Maybe you can help him with the analysis to speed things up?

        The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

        Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

        In the above example, three columns and two rows contain no galaxies:

        v  v  v
        ...#......
        .......#..
        #.........
        >..........<
        ......#...
        .#........
        .........#
        >..........<
        .......#..
        #...#.....
        ^  ^  ^
        These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

        ....#........
        .........#...
        #............
        .............
        .............
        ........#....
        .#...........
        ............#
        .............
        .............
        .........#...
        #....#.......
        Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

        ....1........
        .........2...
        3............
        .............
        .............
        ........4....
        .5...........
        ............6
        .............
        .............
        .........7...
        8....9.......
        In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

        For example, here is one of the shortest paths between galaxies 5 and 9:

        ....1........
        .........2...
        3............
        .............
        .............
        ........4....
        .5...........
        .##.........6
        ..##.........
        ...##........
        ....##...7...
        8....9.......
        This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

        Between galaxy 1 and galaxy 7: 15
        Between galaxy 3 and galaxy 6: 17
        Between galaxy 8 and galaxy 9: 5
        In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

        Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
        """
        self.grid = tuple(self.stripped_lines)

        self._expand_grid_dense()

        self.visited = set()
        distances: list[tuple[int, int], int] = []
        for start in self._starts_dense():
            self.visited.add(start)
            distances += self._bfs_dense(start)

        return sum(distance[1] for distance in distances)

    def _starts_sparse(self):
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == "#":
                    yield x, y

    def _expand_grid_sparse(self):
        # expand rows
        self.y_offsets = []
        self.x_offsets = []
        y_offset = 0
        x_offset = 0
        for row in self.grid:
            if all(char == "." for char in row):
                self.y_offsets.append(None)
                y_offset += self.multiplier
            else:
                self.y_offsets.append(y_offset)
                y_offset += 1
        for i, _ in enumerate(self.grid[0]):
            if all(row[i] == "." for row in self.grid):
                self.x_offsets.append(None)
                x_offset += self.multiplier
            else:
                self.x_offsets.append(x_offset)
                x_offset += 1

    def _bfs_sparse(self, start: tuple[int, int]) -> list[tuple[int, int], int]:
        sx, sy = start
        distances: list[tuple[int, int], int] = []
        for y, row in enumerate(self.grid):
            for x, char in enumerate(row):
                if char == "#" and (x, y) not in self.visited:
                    distances.append(
                        (
                            (x, y),
                            abs(self.x_offsets[x] - self.x_offsets[sx])
                            + abs(self.y_offsets[y] - self.y_offsets[sy]),
                        )
                    )
        return distances

    def second(self):
        """
        --- Part Two ---
        The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

        Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

        (In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

        Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?
        """
        self.grid = tuple(self.stripped_lines)

        self._expand_grid_sparse()
        self.visited = set()
        distances: list[tuple[int, int], int] = []
        for start in self._starts_sparse():
            self.visited.add(start)
            distances += self._bfs_sparse(start)

        return sum(distance[1] for distance in distances)


if __name__ == "__main__":
    Challenge11(1000000).run()
