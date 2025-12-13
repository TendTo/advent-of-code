from shared import BaseChallenge
from typing import Literal

CHAR = Literal[".", "@"]

ADJ_POS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

class Challenge4(BaseChallenge):
    def first(self) -> int:
        grid: list[list[CHAR]] = []
        pickable = 0
        for line in self.stripped_lines:
            grid.append(list(line))
        for r, row in enumerate(grid):
            for c, col in enumerate(row):
                if col != "@":
                    continue
                neighbors = 0
                for dr, dc in ADJ_POS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < len(grid) and 0 <= nc < len(row):
                        neighbor = grid[nr][nc]
                        if neighbor == "@":
                            neighbors += 1
                if neighbors < 4:
                    pickable += 1
        return pickable

    def second(self) -> int:
        grid: list[list[CHAR]] = []
        for line in self.stripped_lines:
            grid.append(list(line))
        rows = len(grid)
        cols = len(grid[0])
        positions = set()
        positions_to_remove = set()
        for r, row in enumerate(grid):
            for c, col in enumerate(row):
                if col == "@":
                    positions.add((r, c))
        pickable = 0
        while True:
            for pos in positions:
                r, c = pos
                neighbors = 0
                for dr, dc in ADJ_POS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor = grid[nr][nc]
                        if neighbor == "@":
                            neighbors += 1
                if neighbors < 4:
                    pickable += 1
                    grid[r][c] = "."
                    positions_to_remove.add((r, c))
            if not positions_to_remove:
                break
            positions -= positions_to_remove
            positions_to_remove.clear()
        return pickable


if __name__ == "__main__":
    Challenge4().run()
