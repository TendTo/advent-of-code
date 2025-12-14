from shared import BaseChallenge


class Challenge7(BaseChallenge):
    def first(self) -> int:
        total = 0
        pos = set()
        for line in self.stripped_lines:
            if "S" in line:
                pos.add(line.index("S"))
                continue
            for p in pos.copy():
                if line[p] == "^":
                    total += 1
                    pos.remove(p)
                    if p - 1 >= 0:
                        pos.add(p - 1)
                    if p + 1 < len(line):
                        pos.add(p + 1)
        return total

    def second(self) -> int:
        pos: set[int] = set()
        count: list[int] = []
        for line in self.stripped_lines:
            if "S" in line:
                count = [0] * (len(line))
                pos.add(line.index("S"))
                count[line.index("S")] = 1
                continue
            for p in pos.copy():
                if line[p] == "^":
                    pos.remove(p)
                    if p - 1 >= 0:
                        pos.add(p - 1)
                        count[p - 1] += count[p]
                    if p + 1 < len(line):
                        pos.add(p + 1)
                        count[p + 1] += count[p]
                    count[p] = 0
        return sum(count)


if __name__ == "__main__":
    Challenge7().run()
