from shared import BaseChallenge
import math
from functools import lru_cache


class Challenge3(BaseChallenge):
    def first(self) -> int:
        total = 0
        for line in self.stripped_lines:
            first_digit, second_digit = line[0], line[-1]
            first_idx = 0
            for i, c in enumerate(line[1:-1], start=1):
                if c > first_digit:
                    first_digit = c
                    first_idx = i
            for c in line[1 + first_idx : -1]:
                second_digit = max(second_digit, c)
            total += int(first_digit + second_digit)
        return total

    def second(self) -> int:
        total = 0
        for line in self.stripped_lines:
            digits = ["0"] * 12
            indexes = [0] * 12
            for i, c in enumerate(line[:-11]):
                if c > digits[0]:
                    digits[0] = c
                    indexes[0] = i
            for i, _ in enumerate(digits[1:], start=1):
                prev_idx = indexes[i - 1]
                top = len(line) - (11 - i)
                for j, c in enumerate(line[1 + prev_idx : top], start=1 + prev_idx):
                    if c > digits[i]:
                        digits[i] = c
                        indexes[i] = j
            total += int("".join(digits))
        return total


if __name__ == "__main__":
    Challenge3().run()
