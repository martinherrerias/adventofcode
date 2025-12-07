#! /usr/bin/env python3
"""
Advent of Code 2025, day 7
https://adventofcode.com/2025/day/7
"""

import argparse
from pathlib import Path

import numpy as np

START = "S"
# EMPTY = "."
SPLITTER = "^"


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


def count_particles(data: np.array):

    split_count = 0
    particles = 1 * (data[0] == START)
    for row in data[1:]:
        splits = particles * (row == SPLITTER)
        split_count += np.count_nonzero(splits)
        particles = (
            particles * np.logical_not(splits) + shift(splits, 1) + shift(splits, -1)
        )

    return sum(particles), split_count


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    # Generic block-wise
    data = np.array([list(line.strip()) for line in lines])

    paths, splits = count_particles(data)

    if part == 1:
        return splits
    elif part == 2:
        return paths
    else:
        raise ValueError(f"Invalid part number: {part}")


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
