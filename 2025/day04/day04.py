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


def part_1(data: np.array):
    """Find the number of @ surrounded by less than 4 @"""

    USED = '@'
    EMPTY = '.'

    data = np.pad(data, 1, constant_values=EMPTY)

    ncols = data.shape[1]
    data = data.reshape(-1)

    offsets = np.array([1, -1, ncols, -ncols, 1+ncols, 1-ncols, -1+ncols, -1-ncols])
    starts = np.where(data == USED)[0].reshape(-1, 1)

    valid = [sum(data[j + offsets] == USED) < 4 for j in starts]

    return np.sum(valid)


def part_2(data: np.array):
    raise NotImplementedError()


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = f.readlines()

    data = np.array([list(line.strip()) for line in lines])

    if part == 1:
        total = part_1(data)
    elif part == 2:
        total = part_2(data)
    else:
        raise ValueError(f'Invalid part number: {part}')

    return total


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
