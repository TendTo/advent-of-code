from shared import BaseChallenge
from re import findall


class Challenge6(BaseChallenge):
    def first(self) -> int:
        total = 0
        values: list[list[int]] = []
        stripped_lines = tuple(self.stripped_lines)
        for line in stripped_lines[:-1]:
            matches = findall(r"(\d+)", line)
            row = list(map(int, matches))
            if len(values) == 0:
                values = [[] for _ in range(len(row))]
            for j, val in enumerate(row):
                values[j].append(val)
        for vals, op in zip(values, findall(r"(\*|\+)", stripped_lines[-1])):
            if op == "*":
                prod = 1
                for v in vals:
                    prod *= v
                total += prod
            elif op == "+":
                total += sum(vals)
        return total

    def second(self) -> int:
        total = 0
        values: list[list[str]] = []
        lines = tuple(self.lines)
        for line in lines[:-1]:
            if not line.strip():
                continue
            if len(values) == 0:
                values = [[] for _ in range(len(line))]
            for j, val in enumerate(line):
                values[j].append(val)
        values = tuple(map(lambda v: int("".join(v)) if "".join(v).strip() else -1, values[:-1]))
        values_int: list[list[int]] = [[]]
        for v in values:
            if v != -1:
                values_int[-1].append(v)
            else:
                values_int.append([])
        for vals, op in zip(values_int, findall(r"(\*|\+)", lines[-1])):
            if op == "*":
                prod = 1
                for v in vals:
                    prod *= v
                total += prod
            elif op == "+":
                total += sum(vals)
        return total


if __name__ == "__main__":
    Challenge6().run()
