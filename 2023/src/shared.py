import argparse
import sys

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Iterable

    class Args(argparse.Namespace):
        input: str
        output: str
        part: int


class BaseChallenge:
    def __init__(self):
        self.args: "Args" = None

    def run(self):
        self.args = self.get_args()
        if self.args.part in (0, 1):
            self.output_result(self.first(), 1)
        if self.args.part in (0, 2):
            self.output_result(self.second(), 2)

    def first(self) -> "Any":
        raise NotImplementedError()

    def second(self) -> "Any":
        raise NotImplementedError()

    def get_args(self) -> "Args":
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-i",
            "--input",
            help="Input file",
            type=str,
            default="-",
        )
        parser.add_argument(
            "-o",
            "--output",
            help="""
            Output file. If a file is specified, the result will be written to it. 
            Otherwise, it will be printed to stdout. 
            A -<part> will be appended to the file name in order to indicate the part and avoid overwriting.""
            """,
            type=str,
            default="-",
        )
        parser.add_argument(
            "-p",
            "--part",
            help="Part to run. 0 means both",
            type=int,
            choices=[0, 1, 2],
            default=0,
        )

        return parser.parse_args()  # type: ignore

    @property
    def stripped_lines(self) -> "Iterable[str]":
        return (line.strip() for line in self.lines if len(line.strip()) > 0)

    @property
    def lines(self) -> "Iterable[str]":
        if self.args.input == "-":
            return sys.stdin.readlines()
        with open(self.args.input, encoding="utf-8") as f:
            return f.readlines()

    def output_result(self, result: "Any", challenge: int):
        if self.args.output == "-":
            print(result)
        else:
            with open(f"{self.args.output}-{challenge}", "w", encoding="utf-8") as f:
                f.write(f"{result}")
