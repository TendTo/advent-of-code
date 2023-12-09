import sys
from io import StringIO
from typing import Callable

from c1 import Challenge1
from c2 import Challenge2
from c3 import Challenge3
from c4 import Challenge4
from c5 import Challenge5
from c6 import Challenge6
from c7 import Challenge7
from c8 import Challenge8
from c9 import Challenge9


def mock_input(input_str: str = ""):
    old_stdin = sys.stdin
    sys.stdin = StringIO(input_str)
    yield
    sys.stdin = old_stdin


def use_input_fixture(input_str: str = ""):
    def decorator(func: Callable):
        def wrapper():
            for _ in mock_input(input_str):
                func()

        return wrapper

    return decorator


@use_input_fixture(
    input_str="""
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
)
def test_challenge_1_part_1():
    assert Challenge1().first() == 142


@use_input_fixture(
    input_str="""
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
)
def test_challenge_1_part_2():
    assert Challenge1().second() == 281


@use_input_fixture(
    input_str="""
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
)
def test_challenge_2_part_1():
    assert Challenge2().first() == 8


@use_input_fixture(
    input_str="""
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
)
def test_challenge_2_part_2():
    assert Challenge2().second() == 2286


@use_input_fixture(
    input_str="""
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
)
def test_challenge_3_part_1():
    assert Challenge3().first() == 4361


@use_input_fixture(
    input_str="""
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
)
def test_challenge_3_part_2():
    assert Challenge3().second() == 467835


@use_input_fixture(
    input_str="""
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
)
def test_challenge_4_part_1():
    assert Challenge4().first() == 13


@use_input_fixture(
    input_str="""
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
)
def test_challenge_4_part_2():
    assert Challenge4().second() == 30


@use_input_fixture(
    input_str="""
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
)
def test_challenge_5_part_1():
    assert Challenge5().first() == 35


@use_input_fixture(
    input_str="""
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
)
def test_challenge_5_part_2():
    assert Challenge5().second() == 46


@use_input_fixture(
    input_str="""
Time:      7  15   30
Distance:  9  40  200
"""
)
def test_challenge_6_part_1():
    assert Challenge6().first() == 288


@use_input_fixture(
    input_str="""
Time:      7  15   30
Distance:  9  40  200
"""
)
def test_challenge_6_part_2():
    assert Challenge6().second() == 71503


@use_input_fixture(
    input_str="""
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
)
def test_challenge_7_part_1():
    assert Challenge7().first() == 6440


@use_input_fixture(
    input_str="""
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
)
def test_challenge_7_part_2():
    assert Challenge7().second() == 5905


@use_input_fixture(
    input_str="""
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""
)
def test_challenge_8_part_1():
    assert Challenge8().first() == 6


@use_input_fixture(
    input_str="""
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
)
def test_challenge_8_part_2():
    assert Challenge8().second() == 6


@use_input_fixture(
    input_str="""
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
)
def test_challenge_9_part_1():
    assert Challenge9().first() == 114


@use_input_fixture(
    input_str="""
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
)
def test_challenge_9_part_2():
    assert Challenge9().second() == 2


if __name__ == "__main__":
    tests = [val for key, val in globals().items() if key.startswith("test_")]
    for test in tests:
        test()
    print("All tests passed!")
