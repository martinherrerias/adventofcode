#! /usr/bin/env python3
"""
Advent of Code 2025 - https://adventofcode.com/2025/
"""

import argparse
from pathlib import Path

import numpy as np


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


def part_1(row):
    return sum(row)


def part_2(row):
    return sum(row) * 2


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    # Numeric row-wise
    rows = [np.fromstring(line, dtype=int, sep=" ") for line in lines]

    if part == 1:
        values = [part_1(row) for row in rows]
    elif part == 2:
        values = [part_2(row) for row in rows]
    else:
        raise ValueError(f"Invalid part number: {part}")

    total = sum(values)

    # # Generic block-wise
    # data = np.array([list(line.strip()) for line in lines])

    # if part == 1:
    #     total = part_1(data)
    # elif part == 2:
    #     total = part_2(data)
    # else:
    #     raise ValueError(f'Invalid part number: {part}')

    if verbose:
        for i, value in enumerate(values):
            print(f"{rows[i]}: {value}")

    return total


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
