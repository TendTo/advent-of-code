from shared import BaseChallenge
from typing import Generator, Iterable


class Hailstone:
    @classmethod
    def from_line(cls, line: str) -> "Hailstone":
        # 19, 13, 30 @ -2,  1, -2
        start_pos, speed = line.split("@")
        x, y, z = tuple(int(pos) for pos in start_pos.split(","))
        sx, sy, sz = tuple(int(pos) for pos in speed.split(","))
        return cls(x, y, z, sx, sy, sz)

    def __init__(self, x: int, y: int, z: int, sx: int, sy: int, sz: int):
        self.x = x
        self.y = y
        self.z = z
        self.sx = sx
        self.sy = sy
        self.sz = sz
        self.m = self.sy / self.sx
        self.known_term = -self.x * self.m + self.y

    def __repr__(self) -> str:
        return f"Hailstone(x={self.x},y={self.y},z={self.z},sx={self.sx},sy={self.sy},sz={self.sz})"

    def intersection(self, other: "Hailstone") -> tuple[int, int]:
        if other == self:
            raise ValueError("Cannot intersect with self")
        # y = m1 x + b1
        # y = m2 x + b2

        # x = b2 - b1 / (m1 - m2)

        denominator = self.m - other.m
        if denominator == 0:
            return -1, -1
        x = (other.known_term - self.known_term) / (self.m - other.m)
        y = self.m * x + self.known_term
        return x, y

    def is_after(self, x: int) -> bool:
        if x - self.x > 0 and self.sx > 0:
            return True
        if x - self.x < 0 and self.sx < 0:
            return True
        return False


class Challenge24(BaseChallenge):
    def __init__(
        self,
        min_pos: tuple[int, int] = (200000000000000, 200000000000000),
        max_pos: tuple[int, int] = (400000000000000, 400000000000000),
    ):
        super().__init__()
        self.hailstones: tuple[Hailstone] = ()
        self.min_x, self.min_y = min_pos
        self.max_x, self.max_y = max_pos

    def _inside_grid(self, x: float, y: float) -> bool:
        """
        Check if the given position is inside the grid.
        """
        return self.min_x <= x <= self.max_x and self.min_y <= y < self.max_y

    def first(self):
        """ """
        self.hailstones = tuple(
            Hailstone.from_line(line) for line in self.stripped_lines
        )
        total = 0
        for i, I_hailstone in enumerate(self.hailstones):
            for II_hailstone in self.hailstones[i + 1 :]:
                x, y = I_hailstone.intersection(II_hailstone)
                if (
                    self._inside_grid(x, y)
                    and I_hailstone.is_after(x)
                    and II_hailstone.is_after(x)
                ):
                    total += 1
        return total

    def second(self):
        """ """
        self.hailstones = tuple(
            Hailstone.from_line(line) for line in self.stripped_lines
        )
        print(self.hailstones)


if __name__ == "__main__":
    Challenge24().run()
