from shared import BaseChallenge


class Challenge1(BaseChallenge):
    def first(self) -> int:
        total = 0
        value = 50
        for line in self.stripped_lines:
            direction = line[0]
            change = int(line[1:])
            if direction == "L":
                value -= change
            elif direction == "R":
                value += change
            while value < 0:
                value += 100
            while value >= 100:
                value -= 100
            if value == 0:
                total += 1
        return total

    def second(self) -> int:
        total = 0
        value = 50
        for line in self.stripped_lines:
            direction = line[0]
            change = int(line[1:])
            if direction == "L":
                if value == 0:
                    total -= 1
                value -= change
            elif direction == "R":
                value += change
            if value >= 100:
                total += value // 100
                print(f"Before: value={value}, total={total}")
            if value <= 0:
                total += -value // 100 + 1
            while value < 0:
                value += 100
            while value >= 100:
                value -= 100
        return total


if __name__ == "__main__":
    Challenge1().run()
