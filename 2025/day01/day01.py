#! /usr/bin/env python3
"""
Advent of Code 2025 - https://adventofcode.com/2025/
"""

import argparse
from pathlib import Path


class Turn:
    def __init__(self, line: str):

        if line[0] == "R":
            self.direction = 1
        elif line[0] == "L":
            self.direction = -1
        else:
            raise ValueError(f"Unexpected direction: {line}")

        self.clicks = int(line[1:])

    def apply(self, starting_value: int) -> int:
        return (starting_value + self.direction * self.clicks) % 100


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default=Path(__file__).with_suffix(".dat"),
        help="Input file, default: %(default)s",
    )
    parser.add_argument(
        "-p",
        "--part",
        type=int,
        nargs="+",
        default=[1, 2],
        help="Part number(s), default: %(default)s",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def part_1(lines: list[str]) -> int:
    position = 50
    counter = 0

    for r in lines:
        r = r.strip()
        newpos = Turn(r).apply(position)
        counter += newpos == 0
        print(f'From {position}, applied {r} to end at {newpos}')
        position = newpos
    return counter


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    if verbose:
        print(f'Read {len(lines)} from {file}')

    if part == 1:
        result = part_1(lines)
    elif part == 2:
        raise NotImplementedError()
    else:
        raise ValueError(f"Invalid part number: {part}")

    return result


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        result = main(args.file, part, args.verbose)
        print(f"Part {part} result: {result}")
