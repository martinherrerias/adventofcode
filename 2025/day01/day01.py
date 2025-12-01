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
        tmp = starting_value + self.direction * self.clicks
        new_position = tmp % 100
        if self.direction > 0 or starting_value == 0:
            crossings = (self.clicks + starting_value) // 100
        else:
            crossings = (100 - starting_value + self.clicks) // 100
        return new_position, crossings


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


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    if verbose:
        print(f"Read {len(lines)} from {file}")

    position = 50
    zero_counter = 0
    cross_counter = 0

    for r in lines:
        r = r.strip()
        new_position, crossings = Turn(r).apply(position)
        zero_counter += new_position == 0
        cross_counter += crossings
        if verbose:
            print(
                f"from: {position}, applied: {r}, new: {new_position}, "
                f"crosssings: {crossings}"
            )
        position = new_position

    if part == 1:
        return zero_counter
    elif part == 2:
        return cross_counter
    else:
        raise ValueError(f"Invalid part number: {part}")


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        result = main(args.file, part, args.verbose)
        print(f"Part {part} result: {result}")
