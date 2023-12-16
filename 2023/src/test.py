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
from c10 import Challenge10
from c11 import Challenge11
from c12 import Challenge12
from c13 import Challenge13
from c14 import Challenge14
from c15 import Challenge15
from c16 import Challenge16


def mock_input(input_str: str = ""):
    old_stdin = sys.stdin
    sys.stdin = StringIO(input_str)
    old_args = sys.argv
    sys.argv = sys.argv[:1]
    yield
    sys.stdin = old_stdin
    sys.argv = old_args


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


@use_input_fixture(
    input_str="""
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
"""
)
def test_challenge_10_part_1():
    assert Challenge10().first() == 4


@use_input_fixture(
    input_str="""
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""
)
def test_challenge_10_part_1_complex():
    assert Challenge10().first() == 8


@use_input_fixture(
    input_str="""
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
)
def test_challenge_10_part_2():
    assert Challenge10().second() == 4


@use_input_fixture(
    input_str="""
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""
)
def test_challenge_10_part_2_complex():
    assert Challenge10().second() == 8


@use_input_fixture(
    input_str="""
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""
)
def test_challenge_10_part_2_complex_2():
    assert Challenge10().second() == 10


@use_input_fixture(
    input_str="""
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
)
def test_challenge_11_part_1():
    assert Challenge11().first() == 374


@use_input_fixture(
    input_str="""
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
)
def test_challenge_11_part_2_mul_10():
    assert Challenge11(10).second() == 1030


@use_input_fixture(
    input_str="""
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
)
def test_challenge_11_part_2_mul_100():
    assert Challenge11(100).second() == 8410


@use_input_fixture(
    input_str="""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
)
def test_challenge_12_part_1():
    assert Challenge12().first() == 21


@use_input_fixture(
    input_str="""
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
)
def test_challenge_12_part_2():
    assert Challenge12().second() == 525152


@use_input_fixture(
    input_str="""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
)
def test_challenge_13_part_1():
    assert Challenge13().first() == 405


@use_input_fixture(
    input_str="""#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#"""
)
def test_challenge_13_part_2():
    assert Challenge13().second() == 400


@use_input_fixture(
    input_str="""
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
)
def test_challenge_14_part_1():
    assert Challenge14().first() == 136


@use_input_fixture(
    input_str="""
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
"""
)
def test_challenge_14_part_1_rolled():
    assert Challenge14().first() == 136


@use_input_fixture(
    input_str="""
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
)
def test_challenge_14_part_2():
    assert Challenge14().second() == 64


@use_input_fixture(
    input_str="""
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
)
def test_challenge_15_part_1():
    assert Challenge15().first() == 1320


@use_input_fixture(
    input_str="""
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
)
def test_challenge_15_part_2():
    assert Challenge15().second() == 145


@use_input_fixture(
    input_str=r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
)
def test_challenge_16_part_1():
    assert Challenge16().first() == 46


@use_input_fixture(
    input_str=r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
)
def test_challenge_16_part_2():
    assert Challenge16().second() == 51


if __name__ == "__main__":
    tests = [val for key, val in globals().items() if key.startswith("test_")]
    for test in tests:
        test()
    print("All tests passed!")
