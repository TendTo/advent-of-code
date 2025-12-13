from shared import BaseChallenge
from dataclasses import dataclass
from sortedcontainers import SortedList


@dataclass
class Range:
    start: int
    end: int

    def __contains__(self, item: int) -> bool:
        return self.start <= item <= self.end

    def __lt__(self, other: "Range") -> bool:
        return self.start < other.start

    def __le__(self, other: "Range") -> bool:
        return self.start <= other.start

    def __gt__(self, other: "Range") -> bool:
        return self.start > other.start

    def __ge__(self, other: "Range") -> bool:
        return self.start >= other.start

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Range):
            return NotImplemented
        return self.start == other.start and self.end == other.end


class RangeMerger:

    def __init__(self):
        self.ranges: SortedList[Range] = SortedList()

    def add_range(self, new_range: Range):
        if len(self.ranges) == 0:
            self.ranges.add(new_range)
            return

        DEFAULT_START_I = -1
        DEFAULT_END_I = len(self.ranges)
        start_i = DEFAULT_START_I
        end_i = DEFAULT_END_I
        for i, existing_range in enumerate(self.ranges):
            start = new_range.start
            end = new_range.end
            if i > start_i and not is_left_of(start, existing_range):
                start_i = i
            if i < end_i and not is_right_of(end, existing_range):
                end_i = i
        if start_i != DEFAULT_START_I and start not in self.ranges[start_i]:
            start_i += 1
        if end_i != DEFAULT_END_I and end not in self.ranges[end_i]:
            end_i -= 1
        if end_i < start_i or start_i == len(self.ranges) or end_i < 0:
            # No overlaps with other ranges, just add it.
            self.ranges.add(new_range)
            return
        # There is some overlap, merge all overlapping ranges into one.
        new_range = Range(
            min(new_range.start, self.ranges[start_i].start if 0 <= start_i < len(self.ranges) else new_range.start),
            max(new_range.end, self.ranges[end_i].end if 0 <= end_i < len(self.ranges) else new_range.end),
        )
        # Normalize indices. We may have gone out of bounds with one or the other
        # but there are definitely ranges to remove.
        start_i = max(0, start_i)
        end_i = min(len(self.ranges) - 1, end_i)
        for _ in range(end_i - start_i + 1):
            # Remove all overlapping ranges.
            self.ranges.pop(start_i)
        # Add the merged range.
        self.ranges.add(new_range)

    @property
    def num_ranges(self) -> int:
        return len(self.ranges)

    @property
    def total_covered(self) -> int:
        total = 0
        for r in self.ranges:
            total += r.end - r.start + 1
        return total


def is_left_of(val: int, rng: Range) -> bool:
    return val < rng.start


def is_right_of(val: int, rng: Range) -> bool:
    return val > rng.end


class Challenge5(BaseChallenge):
    def first(self) -> int:
        ranges: list[Range] = []
        valid = 0
        for line in self.stripped_lines:
            if "-" in line:
                ranges.append(Range(*map(int, line.split("-"))))
            else:
                val = int(line)
                for r in ranges:
                    if r.start <= val <= r.end:
                        valid += 1
                        break
        return valid

    def second(self) -> int:
        ranges: RangeMerger = RangeMerger()
        for i, line in enumerate(self.stripped_lines):
            if "-" in line:
                ranges.add_range(Range(*map(int, line.split("-"))))
            else:
                break
        return ranges.total_covered


if __name__ == "__main__":
    Challenge5().run()
