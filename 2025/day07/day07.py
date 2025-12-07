#! /usr/bin/env python3
"""
Advent of Code 2025, day 7
https://adventofcode.com/2025/day/7
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


def shift(x, n, **kwargs):
    N = abs(n)
    return np.roll(np.pad(x, N, **kwargs), n)[N:-N]


def count_splits(data):

    START = "S"
    # EMPTY = "."
    SPLITTER = "^"

    has_beam = data[0] == START
    split_count = 0
    for row in data[1:]:
        splits = np.logical_and(row == SPLITTER, has_beam)
        split_count += sum(splits)

        has_beam = np.logical_or(
            np.logical_and(has_beam, np.logical_not(splits)),
            np.logical_or(shift(splits, 1), shift(splits, -1)),
        )

    return split_count


def part_2(data):
    raise NotImplementedError()


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    # Generic block-wise
    data = np.array([list(line.strip()) for line in lines])

    if part == 1:
        total = count_splits(data)
    elif part == 2:
        total = part_2(data)
    else:
        raise ValueError(f"Invalid part number: {part}")

    return total


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
