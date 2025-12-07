from shared import BaseChallenge
import math
from functools import lru_cache

class Challenge2(BaseChallenge):
    def first(self) -> int:
        total = 0
        for line in self.stripped_lines:
            ranges = line.split(",")
            for r in ranges:
                range_start, range_end = map(int, r.split("-"))
                v = range_start
                while v <= range_end:
                    str_v = str(v)
                    mid = len(str_v) // 2
                    left = str_v[:mid]
                    right = str_v[mid:]
                    if left == right:
                        total += v
                    v += 1
        return total

    def second(self) -> int:
        total = 0
        for line in self.stripped_lines:
            ranges = line.split(",")
            for r in ranges:
                range_start, range_end = map(int, r.split("-"))
                for v in range(range_start, range_end + 1):
                    if v < 10:
                        continue
                    if not self.is_valid_id(v):
                        total += v
        return total
    
    @lru_cache(maxsize=None)
    def get_factors(self, n: int) -> list[int]:
        factors = set()
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                factors.add(i)
                factors.add(n // i)
        return sorted(factors) + [n]
    
    def is_valid_id(self, v: int) -> bool:
        str_v = str(v)
        length = len(str_v)
        for factor in self.get_factors(length):
            offset = length // factor
            pattern = str_v[:offset]
            is_invalid = False
            for i in range(offset, len(str_v), offset):
                if str_v[i:i + offset] != pattern:
                    break
            else:
                is_invalid = True
            if is_invalid:
                return False
        return True

if __name__ == "__main__":
    Challenge2().run()
