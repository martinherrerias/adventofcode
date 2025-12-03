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


def max_joltage(nums):
    n = len(nums)
    idx1 = np.argmax(nums)
    if idx1 == n - 1:
        newidx = np.argmax(nums[0:n-1])
        if nums[newidx] > 0:
            idx1 = newidx
            idx2 = np.argmax(nums[newidx+1:]) + newidx + 1
        else:
            idx2 = idx1
            idx1 = newidx
    else:
        idx2 = np.argmax(nums[idx1+1:]) + idx1 + 1
    return 10*nums[idx1] + nums[idx2]


def part_2(row):
    return sum(row) * 2


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    # Numeric row-wise
    rows = [list(map(int, list(line.strip()))) for line in lines if line.strip()]

    if part == 1:
        values = [max_joltage(row) for row in rows]
    elif part == 2:
        raise NotImplementedError()
    else:
        raise ValueError(f"Invalid part number: {part}")

    total = sum(values)

    if verbose:
        for i, value in enumerate(values):
            print(f"{rows[i]}: {value}")

    return total


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
