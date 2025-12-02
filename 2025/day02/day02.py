#! /usr/bin/env python3
"""
Advent of Code 2025 - https://adventofcode.com/2025/
"""

import re
from math import ceil, floor
import argparse
from pathlib import Path


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


def find_twin_numbers(id_range: str) -> list[int]:
    """
    Find all numbers in range that consist of a sequence repeated twice
    """
    return find_rep_numbers(id_range, N=2)


def find_rep_numbers(id_range: str, N=None) -> list[int]:
    """
    Find all numbers in a range that consist of one or more repeated digits
    """
    lo, hi = map(int, id_range.split('-'))
    dlo, dhi = map(len, id_range.split('-'))

    bad = []
    for d in range(1, dhi//2 + 1):
        if N is not None:
            n_range = [N]
        else:
            n_range = range(max(2, ceil(dlo / d)), dhi // d + 1)
        for n in n_range:
            b = 10**(d-1)
            b = int(str(b) * n) / b  # e.g. 10.1010 for n=3, d=2
            klo = max(10**(d-1), ceil(lo / b))
            khi = min(10**d-1, floor(hi / b))
            bad.extend([int(k * b) for k in range(klo, khi + 1)])
    return set(bad)


def main(file=None, part=None, verbose=False):

    with open(file, encoding="utf-8") as f:
        lines = ''.join(f.readlines()).replace('\n', '')

    ranges = re.split(',', lines)

    if part == 1:
        return sum(map(lambda x: sum(find_twin_numbers(x)), ranges))
    elif part == 2:
        return sum(map(lambda x: sum(find_rep_numbers(x)), ranges))
    else:
        raise ValueError(f"Invalid part number: {part}")


if __name__ == "__main__":

    args = parse_args()
    for part in args.part:
        total = main(args.file, part, args.verbose)
        print(f"Part {part} total: {total}")
