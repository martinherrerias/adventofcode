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


def max_joltage(nums, digits=2):

    assert not any(n <= 0 for n in nums)

    maxj = 0

    n = len(nums)
    last_used = -1
    for d in range(0, digits):
        idx = np.argmax(nums[last_used + 1 : n - digits + d + 1]) + last_used + 1
        last_used = idx
        maxj = 10 * maxj + nums[idx]

    return maxj


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    # Numeric row-wise
    rows = [list(map(int, list(line.strip()))) for line in lines if line.strip()]

    if part == 1:
        values = [max_joltage(row, 2) for row in rows]
    elif part == 2:
        values = [max_joltage(row, 12) for row in rows]
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
