from shared import BaseChallenge
from typing import Callable
import re


class Part:
    def __init__(self, line: str):
        matches = re.findall(r"\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}", line)
        if len(matches) == 0:
            raise ValueError(f"Invalid input: {line}")
        self.x = int(matches[0][0])
        self.m = int(matches[0][1])
        self.a = int(matches[0][2])
        self.s = int(matches[0][3])

    @property
    def value(self):
        return self.x + self.m + self.a + self.s

    def __repr__(self):
        return f"Part(x={self.x}, m={self.m}, a={self.a}, s={self.s})"


class Check:
    GETTERS: dict[str, Callable[[Part], int]] = {
        "x": lambda p: p.x,
        "m": lambda p: p.m,
        "a": lambda p: p.a,
        "s": lambda p: p.s,
    }

    def __init__(self, check: str):
        if ":" not in check:
            self.getter: Callable[[Part], int] = lambda _: 0
            self.op: Callable[[int], bool] = lambda _: True
            self.destination: str = check
            return

        first, self.destination = check.split(":")
        section, value = first.split("<") if "<" in first else first.split(">")
        self.op = self._get_op("<" if "<" in first else ">", int(value))
        self.getter = self.GETTERS[section]

    def _get_op(self, op: str, value: int) -> Callable[[int], bool]:
        return {
            "<": lambda x: x < value,
            ">": lambda x: x > value,
        }[op]

    def evaluate_part(self, part: Part) -> str | None:
        val = self.getter(part)
        if self.op(val):
            return self.destination
        return None

    def __repr__(self) -> str:
        return f"Check(-> {self.destination})"


class Rule:
    def __init__(self, line: str):
        self.label, checks = line.split("{")
        self.checks = [Check(check) for check in checks[:-1].split(",")]

    def evaluate_part(self, part: Part) -> str:
        for check in self.checks:
            if (next_rule := check.evaluate_part(part)) is not None:
                return next_rule
        raise RuntimeError("should not be reachable")

    def __repr__(self) -> str:
        return f"Rule(label={self.label},checks={self.checks})"


class Challenge19(BaseChallenge):
    def __init__(self):
        super().__init__()
        self.rules: dict[str, Rule] = {}
        self.parts: list[Part] = []

    def first(self):
        """ """
        self.rules = {}
        self.parts = []

        reading_parts = False
        for line in self.lines:
            line = line.strip()
            if len(line) == 0:
                reading_parts = True
                continue

            if reading_parts:
                self.parts.append(Part(line))
            else:
                rule = Rule(line)
                self.rules[rule.label] = rule

        accepted = set()
        for part in self.parts:
            current_rule = "in"
            while current_rule not in ("A", "R"):
                current_rule = self.rules[current_rule].evaluate_part(part)
            if current_rule == "A":
                accepted.add(part)

        return sum(part.value for part in accepted)

    def second(self):
        """ """
        self.rules = {}
        self.parts = []

        reading_parts = False
        for line in self.lines:
            line = line.strip()
            if len(line) == 0:
                reading_parts = True
                continue

            if reading_parts:
                self.parts.append(Part(line))
            else:
                rule = Rule(line)
                self.rules[rule.label] = rule

        accepted = set()
        for part in self.parts:
            current_rule = "in"
            while current_rule not in ("A", "R"):
                current_rule = self.rules[current_rule].evaluate_part(part)
            if current_rule == "A":
                accepted.add(part)

        return sum(part.value for part in accepted)


if __name__ == "__main__":
    Challenge19().run()
